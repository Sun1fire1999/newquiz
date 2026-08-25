# app.py
import streamlit as st
import pandas as pd
import numpy as np
import random
from data.materials import MATERIALS
from data.questions import QUESTIONS

# ======= إعدادات الصفحة =======
st.set_page_config(
    page_title="نظام التدريب على قانون العمل الأردني",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======= CSS مخصص =======
st.markdown("""
<style>
    .main-title { text-align: center; font-size: 2.5em; color: #2E4053; font-weight: bold; margin-bottom: 20px; padding: 10px; background: linear-gradient(90deg, #F8F9FA, #E9ECEF); border-radius: 10px; border-right: 5px solid #2980B9; }
    .article-box { background: #F8F9FA; padding: 15px; border-radius: 5px; border-right: 4px solid #2980B9; margin: 10px 0; }
    .article-title { font-size: 1.2em; font-weight: bold; color: #2980B9; margin-bottom: 5px; }
    .question-box { background: #FFFFFF; padding: 20px; border-radius: 10px; border: 1px solid #E0E0E0; margin: 10px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    .badge { display: inline-block; padding: 3px 10px; border-radius: 15px; font-size: 0.8em; margin: 2px; color: white; }
    .badge-easy { background: #27AE60; }
    .badge-medium { background: #F39C12; }
    .badge-hard { background: #E74C3C; }
    .badge-high { background: #2980B9; }
    .badge-med { background: #7F8C8D; }
    .badge-low { background: #95A5A6; }
    .score-box { background: #F39C12; padding: 10px; border-radius: 10px; text-align: center; font-size: 1.5em; font-weight: bold; color: white; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

# ======= إدارة الحالة =======
if 'quiz_questions' not in st.session_state:
    st.session_state.quiz_questions = []
if 'quiz_index' not in st.session_state:
    st.session_state.quiz_index = 0
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0
if 'quiz_answered' not in st.session_state:
    st.session_state.quiz_answered = False
if 'quiz_selected' not in st.session_state:
    st.session_state.quiz_selected = None
if 'quiz_total' not in st.session_state:
    st.session_state.quiz_total = 0
if 'quiz_history' not in st.session_state:
    st.session_state.quiz_history = []  # سيحتوي على إجابات الأسئلة: [{'index': idx, 'selected': option, 'correct': bool}]

# ======= تحويل الأسئلة إلى DataFrame =======
questions_df = pd.DataFrame(QUESTIONS)

# ======= العنوان الرئيسي =======
st.markdown('<div class="main-title">📚 نظام التدريب على اختبار قانون العمل الأردني رقم (8) لسنة 1996</div>', unsafe_allow_html=True)
st.markdown("### وتعديلاته - 600 سؤال تفاعلي")

# ======= الشريط الجانبي =======
with st.sidebar:
    st.markdown("## 🧭 التنقل")
    page = st.radio("اختر الصفحة", ["📖 المحتوى القانوني", "❓ بنك الأسئلة (600 سؤال)", "🎯 وضع الاختبار", "📊 الإحصائيات"])
    
    st.markdown("---")
    st.markdown("### 📊 نظرة عامة")
    st.write(f"**عدد الأسئلة:** {len(QUESTIONS)}")
    st.write(f"**عدد المحاور:** {questions_df['topic'].nunique()}")
    st.write(f"**عدد المواد:** {len(MATERIALS)}")
    
    st.markdown("---")
    st.markdown("### 🏷️ مستوى الصعوبة")
    if 'difficulty' in questions_df.columns:
        difficulty_counts = questions_df['difficulty'].value_counts()
        for diff, count in difficulty_counts.items():
            st.write(f"- {diff}: {count}")

# ======= الصفحة 1: المحتوى القانوني =======
if page == "📖 المحتوى القانوني":
    st.markdown("## 📖 عرض المواد القانونية")
    
    topics = list(MATERIALS.keys())
    selected_topic = st.selectbox("اختر المحور", topics)
    st.markdown(f"### 📂 محور: {selected_topic}")
    
    for article, content in MATERIALS[selected_topic].items():
        if isinstance(content, dict):
            st.markdown(f'<div class="article-box"><div class="article-title">{article}</div>', unsafe_allow_html=True)
            for key, value in content.items():
                st.write(f"**{key}:** {value}")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="article-box"><div class="article-title">{article}</div>{content}</div>', unsafe_allow_html=True)

# ======= الصفحة 2: بنك الأسئلة =======
elif page == "❓ بنك الأسئلة (600 سؤال)":
    st.markdown("## ❓ بنك الأسئلة")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_topics = st.multiselect("المحور", questions_df['topic'].unique(), default=questions_df['topic'].unique()[:5])
    with col2:
        selected_difficulty = st.multiselect("مستوى الصعوبة", questions_df['difficulty'].unique(), default=questions_df['difficulty'].unique())
    with col3:
        selected_probability = st.multiselect("احتمالية الظهور", questions_df['probability'].unique(), default=questions_df['probability'].unique())
    
    filtered_df = questions_df[
        (questions_df['topic'].isin(selected_topics)) &
        (questions_df['difficulty'].isin(selected_difficulty)) &
        (questions_df['probability'].isin(selected_probability))
    ]
    
    st.write(f"**عدد الأسئلة المطابقة:** {len(filtered_df)}")
    
    for idx, row in filtered_df.iterrows():
        with st.container():
            st.markdown(f'<div class="question-box">', unsafe_allow_html=True)
            diff_badge = {"سهل": "badge-easy", "متوسط": "badge-medium", "صعب": "badge-hard"}.get(row['difficulty'], "badge-easy")
            prob_badge = {"عالية": "badge-high", "متوسطة": "badge-med", "منخفضة": "badge-low"}.get(row['probability'], "badge-med")
            st.markdown(f"<span class='badge {diff_badge}'>{row['difficulty']}</span> <span class='badge {prob_badge}'>احتمالية: {row['probability']}</span> <span class='badge badge-high'>{row['topic']}</span>", unsafe_allow_html=True)
            st.markdown(f"**سؤال {row['id']}:** {row['question']}")
            st.markdown(f"**المادة المرجعية:** {row['article']}")
            
            with st.expander("عرض الإجابة"):
                st.write(f"**الإجابة الصحيحة:** {row['options'][row['correct_answer']]}")
                if row.get('explanation'):
                    st.info(f"**التوضيح:** {row['explanation']}")
            
            st.markdown('</div>', unsafe_allow_html=True)

# ======= الصفحة 3: وضع الاختبار =======
elif page == "🎯 وضع الاختبار":
    st.markdown("## 🎯 وضع الاختبار التفاعلي")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        num_questions = st.slider("عدد الأسئلة", 5, 50, 10)
    with col2:
        quiz_difficulty = st.selectbox("مستوى الصعوبة", ["الكل", "سهل", "متوسط", "صعب"])
    with col3:
        quiz_topic = st.selectbox("المحور", ["الكل"] + list(questions_df['topic'].unique()))
    
    if st.button("🚀 بدء الاختبار"):
        filtered = questions_df.copy()
        if quiz_difficulty != "الكل":
            filtered = filtered[filtered['difficulty'] == quiz_difficulty]
        if quiz_topic != "الكل":
            filtered = filtered[filtered['topic'] == quiz_topic]
        
        selected = filtered.sample(min(num_questions, len(filtered)), random_state=42).to_dict('records')
        st.session_state.quiz_questions = selected
        st.session_state.quiz_index = 0
        st.session_state.quiz_score = 0
        st.session_state.quiz_total = len(selected)
        st.session_state.quiz_answered = False
        st.session_state.quiz_selected = None
        st.session_state.quiz_history = []
        
        st.success(f"تم بدء الاختبار! عدد الأسئلة: {len(selected)}")
    
    if st.session_state.quiz_questions:
        q_idx = st.session_state.quiz_index
        current_q = st.session_state.quiz_questions[q_idx]
        
        st.markdown("---")
        st.markdown(f"### السؤال {q_idx + 1} من {st.session_state.quiz_total}")
        st.progress((q_idx + 1) / st.session_state.quiz_total)
        
        st.markdown(f"**السؤال:** {current_q['question']}")
        
        # التحقق من وجود إجابة سابقة لهذا السؤال في التاريخ
        previous_entry = None
        for entry in st.session_state.quiz_history:
            if entry['index'] == q_idx:
                previous_entry = entry
                break
        
        # تحديد الفهرس الافتراضي للخيار في حالة وجود إجابة سابقة
        default_index = None
        if previous_entry:
            selected_option = previous_entry['selected']
            if selected_option in current_q['options']:
                default_index = current_q['options'].index(selected_option)
        
        options = current_q['options']
        user_choice = st.radio(
            "اختر الإجابة:",
            options,
            key=f"q_{q_idx}",
            index=default_index,
            disabled=False  # نسمح بالتعديل حتى بعد التحقق (للسماح بتغيير الإجابة عند الرجوع)
        )
        
        col1, col2 = st.columns([1, 1])
        with col1:
            # زر التحقق: يظهر دائماً، ويقوم بتحديث السجل وإعادة حساب النتيجة
            if st.button("✅ تحقق من الإجابة", key=f"check_{q_idx}"):
                if user_choice is not None:
                    # إزالة الإجابة السابقة لهذا السؤال إن وجدت
                    st.session_state.quiz_history = [e for e in st.session_state.quiz_history if e['index'] != q_idx]
                    correct_option = options[current_q['correct_answer']]
                    is_correct = (user_choice == correct_option)
                    # إضافة الإجابة الجديدة
                    st.session_state.quiz_history.append({
                        'index': q_idx,
                        'selected': user_choice,
                        'correct': is_correct
                    })
                    # إعادة حساب النتيجة من السجل
                    st.session_state.quiz_score = sum(1 for e in st.session_state.quiz_history if e['correct'])
                    
                    if is_correct:
                        st.success("🎉 إجابة صحيحة!")
                    else:
                        st.error(f"❌ إجابة خاطئة. الإجابة الصحيحة: {correct_option}")
                else:
                    st.warning("⚠️ الرجاء اختيار إجابة أولاً.")
        
        with col2:
            # أزرار التنقل بين الأسئلة
            if st.session_state.quiz_history and any(e['index'] == q_idx for e in st.session_state.quiz_history):
                # إذا تم التحقق من هذا السؤال (موجود في السجل) نعرض أزرار التنقل
                if q_idx > 0:
                    if st.button("⬅️ السؤال السابق", key=f"prev_{q_idx}"):
                        st.session_state.quiz_index = q_idx - 1
                        st.rerun()
                
                # زر التالي أو إنهاء الاختبار
                if q_idx < st.session_state.quiz_total - 1:
                    if st.button("السؤال التالي ⏭️", key=f"next_{q_idx}"):
                        st.session_state.quiz_index = q_idx + 1
                        st.rerun()
                else:
                    if st.button("🏁 إنهاء الاختبار", key=f"finish_{q_idx}"):
                        # عند الإنهاء، نعرض النتيجة النهائية
                        st.session_state.quiz_questions = []
                        st.session_state.quiz_index = 0
                        st.session_state.quiz_score = sum(1 for e in st.session_state.quiz_history if e['correct'])
                        st.session_state.quiz_total = 0
                        st.success(f"🏁 انتهى الاختبار! نتيجتك النهائية: {st.session_state.quiz_score}")
        
        # عرض النتيجة الحالية دائمًا
        if st.session_state.quiz_total > 0:
            st.markdown("---")
            st.markdown(f'<div class="score-box">النتيجة الحالية: {st.session_state.quiz_score} / {st.session_state.quiz_total}</div>', unsafe_allow_html=True)

# ======= الصفحة 4: الإحصائيات =======
elif page == "📊 الإحصائيات":
    st.markdown("## 📊 إحصائيات بنك الأسئلة")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("إجمالي الأسئلة", len(QUESTIONS))
    with col2:
        st.metric("عدد المحاور", questions_df['topic'].nunique())
    with col3:
        st.metric("عدد المواد", len(MATERIALS))
    
    st.markdown("### 📈 توزيع الأسئلة حسب المستوى")
    difficulty_counts = questions_df['difficulty'].value_counts()
    st.bar_chart(difficulty_counts)
    
    st.markdown("### 📈 توزيع الأسئلة حسب الاحتمالية")
    prob_counts = questions_df['probability'].value_counts()
    st.bar_chart(prob_counts)
    
    st.markdown("### 📈 الأسئلة حسب المحور")
    topic_counts = questions_df['topic'].value_counts().reset_index()
    topic_counts.columns = ['المحور', 'العدد']
    st.dataframe(topic_counts)
    
    st.markdown("### 📝 إجمالي الأسئلة المقترحة")
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #2980B9, #27AE60); padding: 20px; border-radius: 10px; color: white; text-align: center;">
        <h2>إجمالي الأسئلة المحتملة: <span style="font-size: 2.5em; font-weight: bold;">{len(QUESTIONS)}+</span></h2>
        <p>تم إنشاء 600 سؤالاً</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 📚 مرجع: قانون العمل الأردني رقم (8) لسنة 1996 وتعديلاته")
st.markdown("تم إنشاء هذا النظام لأغراض التدريب والاختبار فقط. يرجى الرجوع إلى النص الرسمي للقانون عند الحاجة.")