import streamlit as st
from google import genai

st.set_page_config(page_title="Fakhr AI", page_icon="🤖")

st.title("تطبيق فخر الذكاء الاصطناعي 🤖")
st.caption("مشروع إعداد: طلال العنزي / يوسف العنزي / تركي الظفيري / فايز العنزي")

api_key = st.sidebar.text_input("أدخل مفتاح Gemini API:", type="password")

if not api_key:
    st.info("💡 من القائمة الجانبية لتشغيل التطبيق يرجى إدخال مفتاح API الخاص بك.")
else:
    try:
        # تهيئة العميل بالمكتبة الجديدة الرسمية
        client = genai.Client(api_key=api_key)

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # عرض الرسائل السابقة
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # استقبال النص من المستخدم
        if prompt := st.chat_input("اكتب سؤالك هنا..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                # استدعاء النموذج الجديد المباشر
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.error(f"حدث خطأ أثناء الاتصال: {e}")
