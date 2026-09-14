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
    try:
        # تهيئة المكتبة باستخدام المفتاح المدخل
        genai.configure(api_key=api_key)
        
        # البحث المباشر عن نموذج يدعم توليد النصوص بالحساب
        available_models = [
            m.name for m in genai.list_models() 
            if 'generateContent' in m.supported_generation_methods
        ]
        
        # اختيار النموذج المناسب تلقائياً
        selected_model = None
        for target in ["models/gemini-1.5-flash", "models/gemini-1.5-pro", "models/gemini-pro"]:
            if target in available_models:
                selected_model = target
                break
        
        if not selected_model and available_models:
            selected_model = available_models[0]

        if selected_model:
            model = genai.GenerativeModel(selected_model)

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
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
        else:
            st.error("لم يتم العثور على أي نموذج مدعوم لهذا المفتاح.")
            
    except Exception as e:
        st.error(f"حدث خطأ أثناء الاتصال بالخدمة: {e}")
