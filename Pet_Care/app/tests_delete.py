from app import create_app
from app.database import init_db, create_user, create_lost_found_report
from werkzeug.security import generate_password_hash

app = create_app()
db = app.config['AUTH_DB_PATH']
init_db(db)
# create users
owner_id = create_user('Owner','owner@example.com',generate_password_hash('pw'),db)
attacker_id = create_user('Attacker','attacker@example.com',generate_password_hash('pw'),db)
admin_id = create_user('Admin','admin@example.com',generate_password_hash('pw'),db)
# create a report as owner
report_id = create_lost_found_report(owner_id,'lost','Rex','Dog','Labrador','Park','2026-06-01','Nice dog','owner@example.com','$0',None,db)
print('report created', report_id)
# attempt delete as attacker
client = app.test_client()
with client.session_transaction() as s:
    s['user_id'] = attacker_id
    s['user_name'] = 'Attacker'
    s['user_email'] = 'attacker@example.com'
resp = client.post(f'/lost-found/{report_id}/delete', follow_redirects=True)
print('attacker status', resp.status_code)
print('attacker body contains permission?', "You don't have permission" in resp.get_data(as_text=True))
# delete as owner
with client.session_transaction() as s:
    s['user_id'] = owner_id
    s['user_name'] = 'Owner'
    s['user_email'] = 'owner@example.com'
resp2 = client.post(f'/lost-found/{report_id}/delete', follow_redirects=True)
print('owner status', resp2.status_code)
print('owner body contains deleted?', 'Report deleted.' in resp2.get_data(as_text=True))
# recreate report and delete as admin
report_id2 = create_lost_found_report(owner_id,'found','Milo','Cat','Siamese','Street','2026-06-02','Found near store','owner@example.com',None,None,db)
with client.session_transaction() as s:
    s['user_id'] = admin_id
    s['user_name'] = 'Admin'
    s['user_email'] = 'admin@example.com'
    s['is_admin'] = True
resp3 = client.post(f'/lost-found/{report_id2}/delete', follow_redirects=True)
print('admin status', resp3.status_code)
print('admin body contains deleted?', 'Report deleted.' in resp3.get_data(as_text=True))
