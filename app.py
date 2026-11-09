import streamlit as st
import os
import tempfile
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, AudioFileClip, vfx
import arabic_reshaper
from bidi.algorithm import get_display
import numpy as np

st.set_page_config(
    page_title="تطبيق صناع المحتوى الاحترافي",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Mobile & Desktop UI Polish
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.6rem;
    }
    .stButton>button:hover {
        background-color: #ff2121;
    }
    .css-1104ytp {
        border-radius: 12px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 التطبيق الاحترافي الشامل لصناع المحتوى")
st.markdown("### تجاوز فلاتر فيسبوك، حماية الملكية، عزل الصوت، تصميم الأغلفة، وتوليد الهاشتاغات الفيروسية.")

# Sidebar Settings
st.sidebar.header("⚙️ إعدادات الهوية والعلامة التجارية")
logo_file = st.sidebar.file_uploader("ارفع شعارك الشفاف (PNG)", type=["png", "jpg"])
logo_opacity = st.sidebar.slider("شفافية اللوجو في الوسط", min_value=0.1, max_value=0.8, value=0.3, step=0.05)
font_file = st.sidebar.file_uploader("ارفع خطاً عربياً مخصصاً (اختياري - TTF)", type=["ttf"])

filter_option = st.sidebar.selectbox(
    "اختر فيلتر الكاميرا البصري (محاكاة Canon / 360)",
    ["فيلتر دافئ (Canon Look)", "فيلتر طبيعي (سحب طفيف بالألوان)", "فيلتر سينمائي بارد", "بدون فيلتر إضافي"]
)

# Tabs Navigation
tab1, tab2, tab3, tab4 = st.tabs([
    "🎬 معالجة الفيديو والبصمة", 
    "🖼️ استخراج وتصميم غلاف الريلز", 
    "📝 الهاشتاغات والمنشورات", 
    "📷 معالجة الصور"
])

with tab1:
    st.header("🎬 معالجة الفيديو وإزالة الأثر الأصلي")
    st.markdown("يقوم التطبيق بقص الأطراف، تغيير البصمة الرقمية (Hash)، مسح البيانات الوصفية (Metadata)، ودمج الصوت.")
    
    video_file = st.file_uploader("اختر فيديو من هاتفك أو جهازك", type=["mp4", "mov", "avi", "mkv"], key="vid")
    audio_file = st.file_uploader("اختر ملف صوتي جديد / موسيقى بديلة (اختياري)", type=["mp3", "wav", "m4a"], key="aud")
    
    audio_mode = st.radio(
        "وضع هندسة الصوت:",
        ["استبدال الصوت الأصلي بالكامل (إزالة صوت التيكتوك/إنستغرام القديم)", "دمج الصوت الجديد مع خفض الصوت الأصلي"]
    )

    caption = st.text_input("النص البارز على واجهة الفيديو (اختياري)", placeholder="اكتب جملة تحفيزية أو عنواناً يظهر أسفل الفيديو...")

    if st.button("🚀 بدء معالجة الفيديو وحماية الملكية", type="primary"):
        if not video_file:
            st.error("الرجاء رفع الفيديو أولاً!")
        else:
            with st.spinner("⏳ جاري معالجة الفيديو، تطبيق الفلتر، هندسة الصوت، وتغيير البصمة الرقمية..."):
                t_vid = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
                t_vid.write(video_file.read())
                t_vid.close()

                logo_path = None
                if logo_file:
                    t_logo = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
                    t_logo.write(logo_file.read())
                    t_logo.close()
                    logo_path = t_logo.name

                audio_path = None
                if audio_file:
                    t_aud = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                    t_aud.write(audio_file.read())
                    t_aud.close()
                    audio_path = t_aud.name

                font_path = None
                if font_file:
                    t_font = tempfile.NamedTemporaryFile(delete=False, suffix=".ttf")
                    t_font.write(font_file.read())
                    t_font.close()
                    font_path = t_font.name

                output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name

                try:
                    video = VideoFileClip(t_vid.name)
                    w, h = video.size

                    # 1. Micro-cropping لتغيير البصمة والأبعاد
                    crop_margin = 4
                    cropped_video = video.crop(x1=crop_margin, y1=crop_margin, x2=w - crop_margin, y2=h - crop_margin)
                    
                    # 2. تغيير السرعة بنسبة بسيطة (1.01x) لتغيير ترددات الصوت والبصمة
                    modified_video = cropped_video.fx(vfx.speedx, 1.01)

                    # 3. الفلتر اللوني (محاكاة الكاميرا)
                    if filter_option == "فيلتر دافئ (Canon Look)":
                        modified_video = modified_video.fx(vfx.colorx, 1.05)
                    elif filter_option == "فيلتر سينمائي بارد":
                        modified_video = modified_video.fx(vfx.colorx, 0.98)
                    else:
                        modified_video = modified_video.fx(vfx.colorx, 1.03)

                    # 4. معالجة الصوت
                    if audio_path and os.path.exists(audio_path):
                        new_audio = AudioFileClip(audio_path)
                        if new_audio.duration > modified_video.duration:
                            new_audio = new_audio.subclip(0, modified_video.duration)
                        
                        if audio_mode == "استبدال الصوت الأصلي بالكامل (إزالة صوت التيكتوك/إنستغرام القديم)":
                            modified_video = modified_video.set_audio(new_audio)
                        else:
                            orig_audio = modified_video.audio
                            if orig_audio:
                                mixed_audio = CompositeVideoClip([orig_audio.volumex(0.3), new_audio.volumex(0.8)])
                                modified_video = modified_video.set_audio(mixed_audio)
                            else:
                                modified_video = modified_video.set_audio(new_audio)

                    clips_to_composite = [modified_video]

                    # 5. اللوجو في وسط الشاشة بشفافية ذكية
                    if logo_path and os.path.exists(logo_path):
                        logo = ImageClip(logo_path).resize(width=int(w * 0.25))
                        logo = logo.set_opacity(logo_opacity)
                        logo = logo.set_duration(modified_video.duration).set_position(("center", "center"))
                        clips_to_composite.append(logo)

                    # 6. النص العربي على واجهة الفيديو
                    if caption:
                        img = Image.new("RGBA", (w - 8, h - 8), (0, 0, 0, 0))
                        draw = ImageDraw.Draw(img)
                        try:
                            font = ImageFont.truetype(font_path, 35) if font_path and os.path.exists(font_path) else ImageFont.load_default()
                        except:
                            font = ImageFont.load_default()

                        reshaped_text = arabic_reshaper.reshape(caption)
                        bidi_text = get_display(reshaped_text)
                        bbox = draw.textbbox((0, 0), bidi_text, font=font)
                        txt_w, txt_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
                        x, y = ((w - 8) - txt_w) / 2, (h - 8) - txt_h - 120

                        for adj_x in range(-2, 3):
                            for adj_y in range(-2, 3):
                                draw.text((x + adj_x, y + adj_y), bidi_text, font=font, fill="black")
                        draw.text((x, y), bidi_text, font=font, fill="white")

                        temp_txt_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
                        img.save(temp_txt_path)
                        text_clip = ImageClip(temp_txt_path).set_duration(modified_video.duration).set_position(("center", "bottom"))
                        clips_to_composite.append(text_clip)

                    final_video = CompositeVideoClip(clips_to_composite)
                    
                    # 7. التصدير بمعايير فيسبوك وإزالة الروابط والبيانات الوصفية بالكامل
                    final_video.write_videofile(
                        output_path,
                        codec="libx264",
                        audio_codec="aac",
                        fps=video.fps,
                        preset="medium",
                        logger=None,
                        ffmpeg_params=["-pix_fmt", "yuv420p", "-movflags", "+faststart", "-map_metadata", "-1"]
                    )

                    st.success("🎉 تم معالجة الفيديو بنجاح وأصبح جاهزاً كفيديو أصلي 100%!")
                    st.video(output_path)
                    with open(output_path, "rb") as f:
                        st.download_button("📥 تحميل الفيديو المعالج للجهاز", f, file_name="native_original_video.mp4", mime="video/mp4")

                except Exception as e:
                    st.error(f"❌ حدث خطأ أثناء المعالجة: {e}")

with tab2:
    st.header("🖼️ استخراج وتصميم غلاف الريلز (Thumbnail)")
    st.markdown("التقاط لقطة احترافية من الفيديو وإضافة عنوان بارز وشعارك لزيادة نسبة النقر والمشاهدات (CTR).")
    
    thumb_video = st.file_uploader("اختر الفيديو لاستخراج الغلاف منه", type=["mp4", "mov", "avi"], key="thumb_vid")
    thumb_title = st.text_input("اكتب العنوان البارز للغلاف (مثلاً: مفاجأة مذهلة لا تفوتك! 🔥)", placeholder="عنوان الغلاف...")
    
    if thumb_video:
        t_vid_thumb = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        t_vid_thumb.write(thumb_video.read())
        t_vid_thumb.close()
        
        vid_clip = VideoFileClip(t_vid_thumb.name)
        duration = vid_clip.duration
        
        time_second = st.slider("اختر توقيت اللقطة (بالثانية):", min_value=0.0, max_value=float(duration), value=min(2.0, float(duration)))
        
        if st.button("🖼️ التقاط وتصميم الغلاف الاحترافي", type="primary"):
            frame = vid_clip.get_frame(time_second)
            img = Image.fromarray(frame)
            
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.15)
            
            if logo_file:
                logo = Image.open(logo_file).convert("RGBA")
                lw = int(img.width * 0.20)
                lh = int((logo.height / logo.width) * lw)
                logo = logo.resize((lw, lh), Image.Resampling.LANCZOS)
                img.paste(logo, (20, 20), logo)

            if thumb_title:
                draw = ImageDraw.Draw(img)
                try:
                    font = ImageFont.truetype(font_path, 45) if font_path and os.path.exists(font_path) else ImageFont.load_default()
                except:
                    font = ImageFont.load_default()
                
                reshaped = arabic_reshaper.reshape(thumb_title)
                bidi_t = get_display(reshaped)
                
                bbox = draw.textbbox((0, 0), bidi_t, font=font)
                tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
                tx, ty = (img.width - tw) / 2, img.height - th - 80
                
                for ax in range(-3, 4):
                    for ay in range(-3, 4):
                        draw.text((tx + ax, ty + ay), bidi_t, font=font, fill="black")
                draw.text((tx, ty), bidi_t, font=font, fill="yellow")

            thumb_out_path = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg").name
            img.save(thumb_out_path, quality=95)
            
            st.success("✅ تم تصدير غلاف الريلز بنجاح!")
            st.image(thumb_out_path, caption="الصورة المصغرة جاهزة للنشر")
            with open(thumb_out_path, "rb") as f:
                st.download_button("📥 تحميل الصورة المصغرة (Thumbnail)", f, file_name="reel_thumbnail.jpg", mime="image/jpeg")

with tab3:
    st.header("📝 مولد المنشورات والهاشتاغات الفيروسية")
    topic_input = st.text_input("ما هو موضوع الفيديو أو المحتوى؟", placeholder="مثلاً: كرة القدم، كوميديا، تقنية، سفر...")
    
    if st.button("✨ توليد النص والهاشتاغات", type="primary"):
        if not topic_input:
            st.warning("الرجاء كتابة موضوع الفيديو أولاً!")
        else:
            st.subheader("📌 اقتراح نص المنشور:")
            post_template = f"🔥 محتوى استثنائي حصري حول ({topic_input}). لا تفوتوا المشاهدة ومشاركة الأصدقاء! 👇✨\n\n🎯 شاركونا بآرائكم في التعليقات ولا تنسوا المتابعة للمزيد!"
            st.code(post_template, language="markdown")

            st.subheader("#️⃣ الهاشتاغات الفيروسية المقترحة لزيادة التفاعل:")
            viral_tags = "#اكسبلور #فيديو_حصري #محتوى_هادف #فيسبوك_ريلز #مغرب #تونس #الجزائر #trending #reels #viral #explore #foryou"
            st.code(viral_tags, language="text")

with tab4:
    st.header("📷 معالجة الصور الثابتة وتعديل البصمة")
    img_file = st.file_uploader("اختر صورة", type=["jpg", "png", "jpeg"], key="img")
    if st.button("🖼️ معالجة الصورة الآن", type="primary"):
        if img_file:
            base_img = Image.open(img_file).convert("RGBA")
            width, height = base_img.size
            enhancer = ImageEnhance.Color(base_img)
            base_img = enhancer.enhance(1.03)

            if logo_file:
                logo = Image.open(logo_file).convert("RGBA")
                lw = int(width * 0.25)
                lh = int((logo.height / logo.width) * lw)
                logo = logo.resize((lw, lh), Image.Resampling.LANCZOS)
                
                r, g, b, a = logo.split()
                a = a.point(lambda i: int(i * logo_opacity))
                logo.putalpha(a)
                pos = ((width - lw) // 2, (height - lh) // 2)
                base_img.paste(logo, pos, logo)

            out_img = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg").name
            base_img.convert("RGB").save(out_img, quality=95)
            st.image(out_img, caption="الصورة المعالجة")
            with open(out_img, "rb") as f:
                st.download_button("📥 تحميل الصورة المعالجة", f, file_name="native_original_image.jpg", mime="image/jpeg")
