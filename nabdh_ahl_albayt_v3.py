import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# ==========================================
# 1. الاتصال بقاعدة البيانات (نفس قاعدتك القديمة)
# ==========================================
connection = sqlite3.connect("nabdh_database.db")
cursor = connection.cursor()

# التأكد من وجود الجدول (حتى لو موجود ما راح يتأثر)
cursor.execute("""
CREATE TABLE IF NOT EXISTS opinions (
id INTEGER PRIMARY KEY AUTOINCREMENT,
comment TEXT NOT NULL,
sentiment TEXT NOT NULL,
category TEXT NOT NULL,
created_at TEXT NOT NULL
)
""")
connection.commit()

# ==========================================
# 2. الكلمات والتصنيفات (نفس الإصدار 1.1)
# ==========================================
positive_words = [
"ممتاز", "رائع", "حلو", "جيد", "جيدة", "جميل", "مريحة", "احب", "مفيد", 
"متعاون", "نظيف", "خوش", "ممتعة", "سريع", "متطورة", "منظم", "مميز"
]

negative_words = [
"سيء", "سيئة", "ضعيف", "ضعيفة", "تعبان", "تعبانة", "صعب", "صعبة", "فاشل", 
"مزعج", "رديء", "متأخر", "غالي", "مشكلة", "مشاكل", "بطيء", "ازدحام", 
"غير مناسب", "يحتاج", "تحتاج", "نقص"
]

categories = {
"الإنترنت": ["انترنت", "الإنترنت", "شبكة", "wifi", "واي فاي"],
"المختبرات": ["مختبر", "المختبرات", "أجهزة", "اجهزة"],
"القاعات": ["قاعة", "القاعات", "تبريد", "مكيف", "مقاعد"],
"التدريس": ["تدريس", "دكتور", "استاذ", "أستاذ", "شرح", "محاضرة"],
"المكتبة": ["مكتبة", "المكتبة", "كتب", "مصادر"],
"الخدمات": ["خدمات", "الخدمات", "نظافة", "مطعم", "كافتيريا"],
"الامتحانات": ["امتحان", "امتحانات", "اختبار", "أسئلة", "اسئلة"]
}

# ==========================================
# 3. دالة تحليل الرأي (نفس الإصدار 1.1)
# ==========================================
def analyze_comment(comment):
    positive_count = 0
    negative_count = 0

    for word in positive_words:
        if word in comment:
            positive_count += 1

    for word in negative_words:
        if word in comment:
            negative_count += 1

    if positive_count > negative_count:
        sentiment = "إيجابي"
    elif negative_count > positive_count:
        sentiment = "سلبي"
    else:
        sentiment = "محايد"

    detected_category = "موضوع غير محدد"
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in comment:
                detected_category = category
                break
        if detected_category != "موضوع غير محدد":
            break

    return sentiment, detected_category

# ==========================================
# 4. دالة الحفظ (اللي راح تشتغل لما تدوس الزر)
# ==========================================
def save_opinion():
    # ناخذ النص من الصندوق
    opinion = text_box.get("1.0", tk.END).strip()
    
    if opinion == "":
        messagebox.showwarning("تنبيه", "اكتب رأيك أولاً عيني!")
        return
    
    # نحلل الرأي
    sentiment, category = analyze_comment(opinion)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # نحفظ بقاعدة البيانات
    cursor.execute("""
    INSERT INTO opinions (comment, sentiment, category, created_at)
    VALUES (?, ?, ?, ?)
    """, (opinion, sentiment, category, current_time))
    connection.commit()
    
    # نطلع رسالة نجاح
    messagebox.showinfo("نجاح", f"تم حفظ الرأي بنجاح!\n\nالتحليل: {sentiment}\nالموضوع: {category}")
    
    # نفرغ الصندوق
    text_box.delete("1.0", tk.END)

# ==========================================
# 5. بناء الواجهة الرسومية
# ==========================================
root = tk.Tk()
root.title("نبض أهل البيت AI - الإصدار 1.2")
root.geometry("450x350")

title_label = tk.Label(root, text="اكتب رأيك هنا عيني:", font=("Arial", 14, "bold"))
title_label.pack(pady=15)

text_box = tk.Text(root, height=6, width=45, font=("Arial", 12))
text_box.pack(pady=10)

submit_button = tk.Button(root, text="إرسال الرأي", font=("Arial", 12, "bold"), bg="lightgreen", command=save_opinion)
submit_button.pack(pady=15)

# تشغيل النافذة
root.mainloop()