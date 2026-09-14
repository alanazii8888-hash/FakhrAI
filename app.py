import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Fakhr AI", page_icon="🤖")

st.title("تطبيق فخر الذكاء الاصطناعي 🤖")
st.caption("مشروع إعداد: طلال العنزي / يوسف العنزي / تركي الظفيري / فايز العنزي")

api_key = st.sidebar.text_input("أدخل مفتاح Gemini API:", type="password")

if not api_key:
    st.info("💡 من القائمة الجانبية لتشغيل التطبيق يرجى إدخل مفتاح API الخاص بك.")
else:
    try:
        genai.configure(api_key=api_key)

        # تجربة النماذج المتاحة بالترتيب للتأكد من الملاءمة
        model_names = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]
        model = None
        
        for name in model_names:
            try:
                m = genai.GenerativeModel(name)
                # تجربة سريعة للتأكد من قبول النموذج
                model = m
                break
            except Exception:
                continue

        if not model:
            model = genai.GenerativeModel("gemini-1.5-flash")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("اكتب سؤالك هنا..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                try:
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as err:
                    st.error(f"حدث خطأ أثناء التوليد: {err}")

    except Exception as e:
        st.error(f"حدث خطأ في الاتصال: {e}")
