import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Fakhr AI", page_icon="🤖")

st.title("تطبيق فخر الذكاء الاصطناعي 🤖")
st.caption("مشروع إعداد: طلال العنزي / يوسف العنزي / تركي الظفيري / فايز العنزي")

# شريط إدخال الـ API Key في القائمة الجانبية
api_key = st.sidebar.text_input("أدخل مفتاح Gemini API:", type="password")

if not api_key:
    st.info("💡 من القائمة الجانبية لتشغيل التطبيق يرجى إدخال مفتاح API الخاص بك.", icon="💡")
else:
    # تهيئة المكتبة باستخدام المفتاح المدخل
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

    # حفظ سجل المحادثة
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # عرض الرسائل السابقة
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # استقبال النص من المستخدم والرد عليه
    if prompt := st.chat_input("اكتب سؤالك هنا..."):
        # عرض رسالة المستخدم
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # توليد رد الذكاء الاصطناعي
        with st.chat_message("assistant"):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال بالخدمة: {e}")
