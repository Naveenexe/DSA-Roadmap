-- Chainline 2.0 Database Functions (SRS 2.0 Section 7.2)
-- Run this script second in the Supabase SQL Editor.

create or replace function _auth(p_username text, p_pin_hash text)
returns uuid language plpgsql security definer set search_path = public as $$
declare v_id uuid; v_pin text;
begin
  select id, pin_hash into v_id, v_pin from app_users where username = lower(p_username);
  if v_id is null then raise exception 'NO_SUCH_USER'; end if;
  if v_pin is not null and p_pin_hash is null then raise exception 'PIN_REQUIRED'; end if;
  if v_pin is not null and v_pin <> p_pin_hash then raise exception 'WRONG_PIN'; end if;
  return v_id;
end $$;

create or replace function register_user(p_username text, p_display_name text, p_pin_hash text,
  p_daily_goal int, p_language text, p_theme text)
returns jsonb language plpgsql security definer set search_path = public as $$
declare v app_users;
begin
  if lower(p_username) !~ '^[a-z0-9_]{3,20}$' then raise exception 'BAD_USERNAME'; end if;
  insert into app_users(username, display_name, pin_hash, daily_goal, language, theme)
  values (lower(p_username), nullif(trim(p_display_name), ''), p_pin_hash,
    coalesce(p_daily_goal, 2), coalesce(p_language, 'java'), coalesce(p_theme, 'light'))
  returning * into v;
  return (to_jsonb(v) - 'pin_hash' - 'id') || jsonb_build_object('has_pin', v.pin_hash is not null);
exception when unique_violation then
  raise exception 'USERNAME_TAKEN';
end $$;

create or replace function login_user(p_username text, p_pin_hash text)
returns jsonb language plpgsql security definer set search_path = public as $$
declare v_id uuid; v app_users;
begin
  v_id := _auth(p_username, p_pin_hash);
  select * into v from app_users where id = v_id;
  return (to_jsonb(v) - 'pin_hash' - 'id') || jsonb_build_object('has_pin', v.pin_hash is not null);
end $$;

create or replace function get_state(p_username text, p_pin_hash text)
returns jsonb language plpgsql security definer set search_path = public as $$
declare v_id uuid;
begin
  v_id := _auth(p_username, p_pin_hash);
  return jsonb_build_object(
    'progress', coalesce((select jsonb_agg(to_jsonb(p) - 'user_id') from progress p where p.user_id = v_id), '[]'::jsonb),
    'reviews',  coalesce((select jsonb_agg(to_jsonb(r) - 'user_id') from reviews r where r.user_id = v_id), '[]'::jsonb),
    'activity', coalesce((select jsonb_agg(to_jsonb(a) - 'user_id') from activity a
                          where a.user_id = v_id and a.day >= current_date - 100), '[]'::jsonb));
end $$;

create or replace function save_progress(p_username text, p_pin_hash text, p_seq int,
  p_status text, p_mistake boolean, p_notes text, p_day date)
returns jsonb language plpgsql security definer set search_path = public as $$
declare v_id uuid; v_old timestamptz;
begin
  v_id := _auth(p_username, p_pin_hash);
  select solved_at into v_old from progress where user_id = v_id and question_seq = p_seq;
  insert into progress(user_id, question_seq, status, mistake, notes, solved_at, updated_at)
  values (v_id, p_seq, p_status, coalesce(p_mistake, false), coalesce(p_notes, ''),
    case when p_status = 'done' then now() end, now())
  on conflict (user_id, question_seq) do update
    set status = excluded.status, mistake = excluded.mistake, notes = excluded.notes,
        solved_at = coalesce(progress.solved_at, excluded.solved_at), updated_at = now();
  if p_status = 'done' and v_old is null then
    insert into activity(user_id, day, solved_count) values (v_id, p_day, 1)
    on conflict (user_id, day) do update set solved_count = activity.solved_count + 1;
  end if;
  return jsonb_build_object('ok', true);
end $$;

create or replace function save_review(p_username text, p_pin_hash text, p_seq int,
  p_due date, p_step int, p_source text)
returns jsonb language plpgsql security definer set search_path = public as $$
declare v_id uuid;
begin
  v_id := _auth(p_username, p_pin_hash);
  insert into reviews(user_id, question_seq, due_date, step, source)
  values (v_id, p_seq, p_due, coalesce(p_step, 0), coalesce(p_source, 'auto'))
  on conflict (user_id, question_seq) do update
    set due_date = excluded.due_date, step = excluded.step, source = excluded.source;
  return jsonb_build_object('ok', true);
end $$;

create or replace function delete_review(p_username text, p_pin_hash text, p_seq int)
returns jsonb language plpgsql security definer set search_path = public as $$
declare v_id uuid;
begin
  v_id := _auth(p_username, p_pin_hash);
  delete from reviews where user_id = v_id and question_seq = p_seq;
  return jsonb_build_object('ok', true);
end $$;

create or replace function save_settings(p_username text, p_pin_hash text, p_display_name text,
  p_daily_goal int, p_language text, p_theme text)
returns jsonb language plpgsql security definer set search_path = public as $$
declare v_id uuid;
begin
  v_id := _auth(p_username, p_pin_hash);
  update app_users set display_name = nullif(trim(p_display_name), ''),
    daily_goal = p_daily_goal, language = p_language, theme = p_theme where id = v_id;
  return jsonb_build_object('ok', true);
end $$;

create or replace function delete_user(p_username text, p_pin_hash text)
returns jsonb language plpgsql security definer set search_path = public as $$
declare v_id uuid;
begin
  v_id := _auth(p_username, p_pin_hash);
  delete from app_users where id = v_id;
  return jsonb_build_object('ok', true);
end $$;

revoke execute on function _auth(text, text) from public, anon, authenticated;
grant execute on function
  register_user(text, text, text, int, text, text),
  login_user(text, text),
  get_state(text, text),
  save_progress(text, text, int, text, boolean, text, date),
  save_review(text, text, int, date, int, text),
  delete_review(text, text, int),
  save_settings(text, text, text, int, text, text),
  delete_user(text, text)
to anon;
