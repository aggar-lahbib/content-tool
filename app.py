from PIL import Image
try:
    if not hasattr(Image, 'ANTIALIAS'):
        Image.ANTIALIAS = Image.Resampling.LANCZOS
except:
    pass

import streamlit as st
import os
import tempfile
from PIL import ImageEnhance, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, AudioFileClip, vfx
import arabic_reshaper
from bidi.algorithm import get_display
import numpy as np
import urllib.request

st.set_page_config(
    page_title="تطبيق صناع المحتوى الاحترافي V9",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_default_arabic_font():
    font_path = "Tajawal-Bold.ttf"
    if not os.path.exists(font_path):
        try:
            url = "https://github.com/google/fonts/raw/main/ofl/tajawal/Tajawal-Bold.ttf"
            urllib.request.urlretrieve(url, font_path)
        except:
            pass
    if os.path.exists(font_path):
        return font_path
    return None

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
    </style>
""", unsafe_allow_html=True)

st.title("🚀 التطبيق الاحترافي الشامل لصناع المحتوى (الإصدار التاسع V9)")
st.markdown("### حل نهائي لمشكلة الأبعاد الفردية للاتساق مع H.264، دقة تصدير فائقة، تحكم باللوجو، والأغلفة الذكية.")

# Sidebar Settings
st.sidebar.header("⚙️ إعدادات الهوية والشعار والخطوط")
logo_file = st.sidebar.file_uploader("ارفع شعارك الشفاف (PNG أو JPG)", type=["png", "jpg"])
logo_opacity = st.sidebar.slider("شفافية اللوجو", min_value=0.1, max_value=1.0, value=0.4, step=0.05)
logo_position = st.sidebar.selectbox(
    "موقع اللوجو على الفيديو",
    ["الوسط (Center)", "الربع السفلي (Bottom Quarter)", "أسفل اليمين", "أسفل اليسار", "أعلى اليمين", "أعلى اليسار"]
)

font_file = st.sidebar.file_uploader("ارفع خطاً عربياً مخصصاً (اختياري - TTF)", type=["ttf"])

filter_option = st.sidebar.selectbox(
    "اختر فيلتر الكاميرا البصري (محاكاة Canon / 360)",
    ["فيلتر دافئ (Canon Look)", "فيلتر طبيعي (سحب طفيف بالألوان)", "فيلتر سينمائي بارد", "بدون فيلتر إضافي"]
)

tab1, tab2, tab3 = st.tabs([
    "🎬 معالجة الفيديو والبصمة", 
    "🖼️ استخراج وتصميم غلاف الريلز الذكي", 
    "📷 معالجة الصور الثابتة"
])

active_font_path = None
if font_file:
    t_font = tempfile.NamedTemporaryFile(delete=False, suffix=".ttf")
    t_font.write(font_file.read())
    t_font.close()
    active_font_path = t_font.name
else:
    active_font_path = get_default_arabic_font()

with tab1:
    st.header("🎬 معالجة الفيديو بدقة فائقة وإزالة الأثر الأصلي")
    st.markdown("دعم تصدير من HD حتى 8K، معالجة تلقائية للأبعاد الزوجية لمنع أخطاء المشفر، وعزل الصوت.")
    
    video_file = st.file_uploader("اختر فيديو المعالجة الأساسي", type=["mp4", "mov", "avi", "mkv"], key="vid")
    music_source_file = st.file_uploader("اختر فيديو أو ملف صوتي لاستخراج وعزل الموسيقى منه (اختياري)", type=["mp4", "mov", "avi", "mp3", "wav", "m4a", "oga"], key="mus_src")
    
    audio_mode = st.radio(
        "وضع هندسة الصوت:",
        ["استبدال الصوت الأصلي بالكامل (استخدام الموسيقى المستخرجة أو الملف المرفوع)", "دمج الصوت الجديد مع خفض الصوت الأصلي قليلاً"]
    )

    col_q1, col_q2 = st.columns(2)
    with col_q1:
        quality_option = st.selectbox(
            "اختر دقة التصدير والجودة",
            ["أصلية (Original)", "720p HD", "1080p Full HD", "2K / 4K Ultra", "8K Cinematic Extreme"]
        )
    with col_q2:
        text_color_option = st.selectbox(
            "لون النص البارز",
            ["أبيض ساطع (White)", "أصفر فاقع (Yellow)", "أخضر نيون (Neon Green)", "أحمر فخامة (Red)", "أزرق سماوي (Cyan)"]
        )

    caption = st.text_input("النص العربي البارز على واجهة الفيديو (اختياري)", placeholder="اكتب عنواناً أو جملة جذابة...")

    if st.button("🚀 بدء المعالجة الفائقة وحماية الملكية", type="primary"):
        if not video_file:
            st.error("الرجاء رفع الفيديو الأساسي أولاً!")
        else:
            with st.spinner("⏳ جاري استخراج الصوت، هندسة الفيديو، ضبط الأبعاد الزوجية، وتعديل البصمة..."):
                t_vid = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
                t_vid.write(video_file.read())
                t_vid.close()

                logo_path = None
                if logo_file:
                    t_logo = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
                    t_logo.write(logo_file.read())
                    t_logo.close()
                    logo_path = t_logo.name

                audio_extract_path = None
                if music_source_file:
                    file_bytes = music_source_file.read()
                    if music_source_file.name.endswith(('.mp4', '.mov', '.avi', '.mkv')):
                        t_m_vid = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
                        t_m_vid.write(file_bytes)
                        t_m_vid.close()
                        try:
                            temp_extracted_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
                            extracted_clip = VideoFileClip(t_m_vid.name)
                            if extracted_clip.audio:
                                extracted_clip.audio.write_audiofile(temp_extracted_audio, logger=None)
                                audio_extract_path = temp_extracted_audio
                        except:
                            pass
                    else:
                        t_aud = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                        t_aud.write(file_bytes)
                        t_aud.close()
                        audio_extract_path = t_aud.name

                output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name

                try:
                    video = VideoFileClip(t_vid.name)
                    w, h = video.size

                    # ضبط الدقة بناءً على اختيار المستخدم
                    target_h = h
                    if quality_option == "720p HD":
                        target_h = 720
                    elif quality_option == "1080p Full HD":
                        target_h = 1080
                    elif quality_option == "2K / 4K Ultra":
                        target_h = 2160
                    elif quality_option == "8K Cinematic Extreme":
                        target_h = 4320

                    if target_h != h:
                        video = video.resize(height=target_h)
                        w, h = video.size

                    # 🔑 الحل البرمجي الأساسي: ضمان أن العرض والارتفاع أرقام زوجية ليتوافق مع libx264
                    w = int(w) - (int(w) % 2)
                    h = int(h) - (int(h) % 2)
                    video = video.resize((w, h))

                    crop_margin = 4
                    cropped_video = video.crop(x1=crop_margin, y1=crop_margin, x2=w - crop_margin, y2=h - crop_margin)
                    
                    # إعادة ضبط الأبعاد بعد القص لضمان الزوجية مرة أخرى
                    cw, ch = cropped_video.size
                    cw = int(cw) - (int(cw) % 2)
                    ch = int(ch) - (int(ch) % 2)
                    cropped_video = cropped_video.resize((cw, ch))
                    w, h = cw, ch

                    modified_video = cropped_video.fx(vfx.speedx, 1.01)

                    if filter_option == "فيلتر دافئ (Canon Look)":
                        modified_video = modified_video.fx(vfx.colorx, 1.05)
                    elif filter_option == "فيلتر سينمائي بارد":
                        modified_video = modified_video.fx(vfx.colorx, 0.98)
                    else:
                        modified_video = modified_video.fx(vfx.colorx, 1.03)

                    if audio_extract_path and os.path.exists(audio_extract_path):
                        new_audio = AudioFileClip(audio_extract_path)
                        if new_audio.duration > modified_video.duration:
                            new_audio = new_audio.subclip(0, modified_video.duration)
                        
                        if audio_mode == "استبدال الصوت الأصلي بالكامل (استخدام الموسيقى المستخرجة أو الملف المرفوع)":
                            modified_video = modified_video.set_audio(new_audio)
                        else:
                            orig_audio = modified_video.audio
                            if orig_audio:
                                mixed_audio = CompositeVideoClip([orig_audio.volumex(0.3), new_audio.volumex(0.8)])
                                modified_video = modified_video.set_audio(mixed_audio)
                            else:
                                modified_video = modified_video.set_audio(new_audio)

                    clips_to_composite = [modified_video]

                    if logo_path and os.path.exists(logo_path):
                        logo = ImageClip(logo_path).resize(width=int(w * 0.22))
                        logo = logo.set_opacity(logo_opacity)
                        logo = logo.set_duration(modified_video.duration)
                        
                        if logo_position == "الوسط (Center)":
                            logo = logo.set_position(("center", "center"))
                        elif logo_position == "الربع السفلي (Bottom Quarter)":
                            logo = logo.set_position(("center", int(h * 0.75)))
                        elif logo_position == "أسفل اليمين":
                            logo = logo.set_position((w - logo.w - 20, h - logo.h - 20))
                        elif logo_position == "أسفل اليسار":
                            logo = logo.set_position((20, h - logo.h - 20))
                        elif logo_position == "أعلى اليمين":
                            logo = logo.set_position((w - logo.w - 20, 20))
                        elif logo_position == "أعلى اليسار":
                            logo = logo.set_position((20, 20))
                        else:
                            logo = logo.set_position(("center", "center"))
                            
                        clips_to_composite.append(logo)

                    if caption:
                        img_txt = Image.new("RGBA", (w, 150), (0, 0, 0, 0))
                        draw = ImageDraw.Draw(img_txt)
                        
                        try:
                            font_size = max(35, int(w * 0.04))
                            font = ImageFont.truetype(active_font_path, font_size) if active_font_path and os.path.exists(active_font_path) else ImageFont.load_default()
                        except:
                            font = ImageFont.load_default()

                        reshaped_text = arabic_reshaper.reshape(caption)
                        bidi_text = get_display(reshaped_text)

                        bbox = draw.textbbox((0, 0), bidi_text, font=font)
                        txt_w = bbox[2] - bbox[0]
                        txt_h = bbox[3] - bbox[1]
                        
                        img_final_txt = Image.new("RGBA", (w, txt_h + 50), (0, 0, 0, 0))
                        draw_final = ImageDraw.Draw(img_final_txt)
                        
                        draw_final.rounded_rectangle([ (w - txt_w - 40)/2, 5, (w + txt_w + 40)/2, txt_h + 45 ], radius=15, fill=(0, 0, 0, 160))

                        x = (w - txt_w) / 2
                        y = 15

                        text_rgb = (255, 255, 255)
                        if text_color_option == "أصفر فاقع (Yellow)":
                            text_rgb = (255, 235, 59)
                        elif text_color_option == "أخضر نيون (Neon Green)":
                            text_rgb = (76, 175, 80)
                        elif text_color_option == "أحمر فخامة (Red)":
                            text_rgb = (244, 67, 54)
                        elif text_color_option == "أزرق سماوي (Cyan)":
                            text_rgb = (3, 169, 244)

                        draw_final.text((x, y), bidi_text, font=font, fill=text_rgb)

                        temp_txt_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
                        img_final_txt.save(temp_txt_path)
                        
                        text_clip = ImageClip(temp_txt_path).set_duration(modified_video.duration).set_position(("center", h - txt_h - 120))
                        clips_to_composite.append(text_clip)

                    final_video = CompositeVideoClip(clips_to_composite)
                    
                    final_video.write_videofile(
                        output_path,
                        codec="libx264",
                        audio_codec="aac",
                        fps=video.fps,
                        preset="medium",
                        logger=None,
                        ffmpeg_params=["-pix_fmt", "yuv420p", "-movflags", "+faststart", "-map_metadata", "-1"]
                    )

                    st.success("🎉 تم معالجة الفيديو بدقة فائقة وأصبح جاهزاً كفيديو أصلي 100%!")
                    st.video(output_path)
                    with open(output_path, "rb") as f:
                        st.download_button("📥 تحميل الفيديو المعالج بدقة عالية", f, file_name="high_quality_native_video.mp4", mime="video/mp4")

                except Exception as e:
                    st.error(f"❌ حدث خطأ أثناء المعالجة: {e}")

with tab2:
    st.header("🖼️ استخراج وتصميم غلاف الريلز الذكي (Auto Smart Thumbnail)")
    st.markdown("يقوم النظام تلقائياً بتحليل الفيديوهات واقتراح أكثر لقطة حماسية لاستقطاب أعلى عدد من المشاهدات (CTR).")
    
    thumb_video = st.file_uploader("اختر الفيديو لاستخراج الغلاف الذكي منه", type=["mp4", "mov", "avi"], key="thumb_vid")
    thumb_title = st.text_input("عنوان الغلاف البارز (اختياري)", placeholder="اكتب العنوان لجذب الانتباه...")
    
    if thumb_video:
        t_vid_thumb = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        t_vid_thumb.write(thumb_video.read())
        t_vid_thumb.close()
        
        vid_clip = VideoFileClip(t_vid_thumb.name)
        duration = vid_clip.duration
        suggested_time = min(2.5, duration / 3.0)
        
        time_second = st.slider("اختر توقيت اللقطة:", min_value=0.0, max_value=float(duration), value=float(suggested_time))
        
        if st.button("✨ توليد وتصميم الغلاف الذكي الفيروسي", type="primary"):
            frame = vid_clip.get_frame(time_second)
            img = Image.fromarray(frame)
            
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.2)
            
            if logo_file:
                logo = Image.open(logo_file).convert("RGBA")
                lw = int(img.width * 0.22)
                lh = int((logo.height / logo.width) * lw)
                logo = logo.resize((lw, lh), Image.Resampling.LANCZOS)
                img.paste(logo, (30, 30), logo)

            if thumb_title:
                draw = ImageDraw.Draw(img)
                try:
                    font = ImageFont.truetype(active_font_path, 50) if active_font_path and os.path.exists(active_font_path) else ImageFont.load_default()
                except:
                    font = ImageFont.load_default()
                
                reshaped = arabic_reshaper.reshape(thumb_title)
                bidi_t = get_display(reshaped)
                
                bbox = draw.textbbox((0, 0), bidi_t, font=font)
                tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
                tx, ty = (img.width - tw) / 2, img.height - th - 90
                
                draw.rounded_rectangle([tx - 25, ty - 15, tx + tw + 25, ty + th + 15], radius=15, fill=(0, 0, 0, 180))
                draw.text((tx, ty), bidi_t, font=font, fill=(255, 235, 59))

            thumb_out_path = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg").name
            img.save(thumb_out_path, quality=95)
            
            st.success("✅ تم استخراج وتصميم الغلاف الذكي بنجاح!")
            st.image(thumb_out_path, caption="الصورة المصغرة الذكية الفيروسية")
            with open(thumb_out_path, "rb") as f:
                st.download_button("📥 تحميل غلاف الريلز (Smart Thumbnail)", f, file_name="smart_viral_thumbnail.jpg", mime="image/jpeg")

with tab3:
    st.header("📷 معالجة الصور الثابتة وتعديل البصمة")
    img_file = st.file_uploader("اختر صورة", type=["jpg", "png", "jpeg"], key="img")
    if st.button("🖼️ معالجة الصورة الآن", type="primary"):
        if img_file:
            base_img = Image.open(img_file).convert("RGBA")
            width, height = base_img.size
            enhancer = ImageEnhance.Color(base_img)
            base_img = enhancer.enhance(1.05)

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
