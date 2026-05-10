def connect_to_sheet():
    import json
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # قراءة النص بالكامل من الخزنة
    json_string = st.secrets["json_creds"]
    creds_info = json.loads(json_string)
    
    # التأكد من معالجة الفواصل في المفتاح السري
    if "private_key" in creds_info:
        creds_info["private_key"] = creds_info["private_key"].replace("\\n", "\n")
        
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_info, scope)
    client = gspread.authorize(creds)
    sheet = client.open("بيانات مشروع الماء حياة 2").sheet1
    return sheet