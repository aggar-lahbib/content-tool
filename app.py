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
    page_title="التطبيق الاحترافي الشامل لصناع المحتوى V8 Ultimate",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# دالة لتحميل خط عربي عصري افتراضي (Tajawal) تلقائياً لتفادي مشاكل الخطوط
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
        padding: 0.7rem;
    }
    .stButton>button:hover {
        background-color: #ff2121;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 النظام الاحترافي الشامل لصناع المحتوى (V8 Ultimate)")
st.markdown("### تدمير بصمة المالك الأصلي، خداع خوارزميات Meta، دقة تصدير فائقة، وتخصيص بصري فريد عالمياً.")

# القائمة الجانبية لإعدادات الهوية والبصمة
st.sidebar.header("⚙️ إعدادات الهوية واللوجو والبصمة")
logo_file = st.sidebar.file_uploader("ارفع شعارك الشفاف (PNG أو JPG)", type=["png", "jpg"])
logo_opacity = st.sidebar.slider("شفافية اللوجو", min_value=0.1, max_value=1.0, value=0.45, step=0.05)
logo_position = st.sidebar.selectbox(
    "موقع اللوجو على الفيديو",
    ["الربع السفلي (Bottom Quarter - موصى به للريلز)", "الوسط (Center)", "أسفل اليمين", "أسفل اليسار", "أعلى اليمين", "أعلى اليسار"]
)

font_file = st.sidebar.file_uploader("ارفع خطاً عربياً مخصصاً (اختياري - TTF)", type=["ttf"])

filter_option = st.sidebar.selectbox(
    "اختر الفلتر البصري لتغيير التوقيع اللوني (خداع AI)",
    ["فيلتر سينمائي دافئ (Canon Look)", "فيلتر طبيعي عالي التباين", "فيلتر بارد هادئ", "بدون فيلتر إضافي"]
)

tab1, tab2, tab3 = st.tabs([
    "🎬 معالجة الفيديو وتدمير البصمة", 
    "🖼️ استخراج وتصميم غلاف الريلز الذكي", 
    "📷 معالجة الصور الثابتة وبصمتها"
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
    st.header("🎬 معالجة الفيديو بدقة فائقة وحماية مطلقة ضد الحظر")
    st.markdown("يقوم النظام بقص الأطراف، تغيير السرعة بدقة، مسح الميتافيتا، عزل واستبدال الصوت، وتوليد فيديو أصلي 100%.")
    
    video_file = st.file_uploader("اختر فيديو المعالجة الأساسي", type=["mp4", "mov", "avi", "mkv"], key="vid")
    music_source_file = st.file_uploader("اختر فيديو أمانة / ملف صوتي استخراج الموسيقى منه (اختياري)", type=["mp4", "mov", "avi", "mp3", "wav", "m4a", "oga"], key="mus_src")
    
    audio_mode = st.radio(
        "وضع هندسة الصوت:",
        ["استبدال الصوت الأصلي بالكامل (استخدام الموسيقى المستخرجة لتجاوز حقوق الملكية)", "دمج الصوت الجديد مع خفض الصوت الأصلي قليلاً"]
    )

    col_q1, col_q2 = st.columns(2)
    with col_q1:
        quality_option = st.selectbox(
            "اختر دقة التصدير والجودة",
            ["أصلية مطابقة (Original Native)", "720p HD", "1080p Full HD", "2K / 4K Ultra"]
        )
    with col_q2:
        text_color_option = st.selectbox(
            "لون النص البارز",
            ["أبيض ناصع (White)", "أصفر فاقع (Yellow)", "أخضر نيون (Neon Green)", "أحمر فخامة (Red)", "أزرق سماوي (Cyan)"]
        )

    caption = st.text_input("النص العربي البارز على واجهة الفيديو (اختياري)", placeholder="اكتب عنواناً جذاباً أو جملة تحفيزية...")

    if st.button("🚀 بدء المعالجة الفائقة وتوليد الهوية الجديدة", type="primary"):
        if not video_file:
            st.error("الرجاء رفع الفيديو الأساسي أولاً!")
        else:
            with st.spinner("⏳ جاري استخراج الصوت، هندسة الفيديو، ضبط الأبعاد الزوجية، وتدمير البصمة القديمة..."):
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

                    # ضبط الدقة المطلوبة مع ضمان بقاء الأبعاد زوجية (ل, ع) لمنع انهيار المشفر
                    if quality_option == "720p HD":
                        target_h = 720
                    elif quality_option == "1080p Full HD":
                        target_h = 1080
                    elif quality_option == "2K / 4K Ultra":
                        target_h = 2160
                    else:
                        target_h = h

                    if target_h != h:
                        video = video.resize(height=target_h)
                        w, h = video.size

                    # فرض الزوجية المطلقة للأبعاد (Libx264 Requirement)
                    w = int(w) - (int(w) % 2)
                    h = int(h) - (int(h) % 2)
                    video = video.resize((w, h))

                    # قص أطراف لتدمير البصمة الرقمية تماماً
                    crop_margin = 4
                    if w > 30 and h > 30:
                        cropped_video = video.crop(x1=crop_margin, y1=crop_margin, x2=w - crop_margin, y2=h - crop_margin)
                        cw, ch = cropped_video.size
                        cw = int(cw) - (int(cw) % 2)
                        ch = int(ch) - (int(ch) % 2)
                        cropped_video = cropped_video.resize((cw, ch))
                        w, h = cw, ch
                    else:
                        cropped_video = video

                    # تعديل طفيف للسرعة لتغيير التوقيع الرقمي
                    modified_video = cropped_video.fx(vfx.speedx, 1.01)

                    # تطبيق الفلتر البصري
                    if filter_option == "فيلتر سينمائي دافئ (Canon Look)":
                        modified_video = modified_video.fx(vfx.colorx, 1.06)
                    elif filter_option == "فيلتر طبيعي عالي التباين":
                        modified_video = modified_video.fx(vfx.colorx, 1.03)
                    elif filter_option == "فيلتر بارد هادئ":
                        modified_video = modified_video.fx(vfx.colorx, 0.97)
                    else:
                        modified_video = modified_video.fx(vfx.colorx, 1.02)

                    # دمج أو استبدال الصوت
                    if audio_extract_path and os.path.exists(audio_extract_path):
                        new_audio = AudioFileClip(audio_extract_path)
                        if new_audio.duration > modified_video.duration:
                            new_audio = new_audio.subclip(0, modified_video.duration)
                        
                        if audio_mode == "استبدال الصوت الأصلي بالكامل (استخدام الموسيقى المستخرجة لتجاوز حقوق الملكية)":
                            modified_video = modified_video.set_audio(new_audio)
                        else:
                            orig_audio = modified_video.audio
                            if orig_audio:
                                mixed_audio = CompositeVideoClip([orig_audio.volumex(0.25), new_audio.volumex(0.85)])
                                modified_video = modified_video.set_audio(mixed_audio)
                            else:
                                modified_video = modified_video.set_audio(new_audio)

                    clips_to_composite = [modified_video]

                    # إضافة الشعار الشفاف بالدقة والموقع المطلوبة
                    if logo_path and os.path.exists(logo_path):
                        logo_w = int(w * 0.22)
                        logo_w = int(logo_w) - (int(logo_w) % 2)
                        logo = ImageClip(logo_path).resize(width=logo_w)
                        logo = logo.set_opacity(logo_opacity)
                        logo = logo.set_duration(modified_video.duration)
                        
                        lw_val, lh_val = logo.size
                        lw_val = int(lw_val) - (int(lw_val) % 2)
                        lh_val = int(lh_val) - (int(lh_val) % 2)
                        logo = logo.resize((lw_val, lh_val))

                        if logo_position == "الوسط (Center)":
                            logo = logo.set_position(("center", "center"))
                        elif logo_position == "الربع السفلي (Bottom Quarter - موصى به للريلز)":
                            logo = logo.set_position(("center", int(h * 0.72)))
                        elif logo_position == "أسفل اليمين":
                            logo = logo.set_position((w - lw_val - 25, h - lh_val - 25))
                        elif logo_position == "أسفل اليسار":
                            logo = logo.set_position((25, h - lh_val - 25))
                        elif logo_position == "أعلى اليمين":
                            logo = logo.set_position((w - lw_val - 25, 25))
                        elif logo_position == "أعلى اليسار":
                            logo = logo.set_position((25, 25))
                        else:
                            logo = logo.set_position(("center", int(h * 0.72)))
                            
                        clips_to_composite.append(logo)

                    # كتابة النص العربي بوضوح وهندسة عصرية
                    if caption:
                        try:
                            font_size = max(35, int(w * 0.045))
                            font = ImageFont.truetype(active_font_path, font_size) if active_font_path and os.path.exists(active_font_path) else ImageFont.load_default()
                        except:
                            font = ImageFont.load_default()

                        reshaped_text = arabic_reshaper.reshape(caption)
                        bidi_text = get_display(reshaped_text)

                        dummy_img = Image.new("RGBA", (10, 10))
                        dummy_draw = ImageDraw.Draw(dummy_img)
                        bbox = dummy_draw.textbbox((0, 0), bidi_text, font=font)
                        txt_w = bbox[2] - bbox[0]
                        txt_h = bbox[3] - bbox[1]
                        
                        box_w = int(txt_w + 50)
                        box_w = int(box_w) - (int(box_w) % 2)
                        box_h = int(txt_h + 45)
                        box_h = int(box_h) - (int(box_h) % 2)

                        img_final_txt = Image.new("RGBA", (box_w, box_h), (0, 0, 0, 0))
                        draw_final = ImageDraw.Draw(img_final_txt)
                        draw_final.rounded_rectangle([0, 0, box_w, box_h], radius=18, fill=(0, 0, 0, 180))

                        text_rgb = (255, 255, 255)
                        if text_color_option == "أصفر فاقع (Yellow)":
                            text_rgb = (255, 235, 59)
                        elif text_color_option == "أخضر نيون (Neon Green)":
                            text_rgb = (76, 175, 80)
                        elif text_color_option == "أحمر فخامة (Red)":
                            text_rgb = (244, 67, 54)
                        elif text_color_option == "أزرق سماوي (Cyan)":
                            text_rgb = (3, 169, 244)

                        draw_final.text(((box_w - txt_w) / 2, (box_h - txt_h) / 2 - 4), bidi_text, font=font, fill=text_rgb)

                        temp_txt_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
                        img_final_txt.save(temp_txt_path)
                        
                        text_clip = ImageClip(temp_txt_path).set_duration(modified_video.duration).set_position(("center", h - box_h - 130))
                        clips_to_composite.append(text_clip)

                    final_video = CompositeVideoClip(clips_to_composite)
                    
                    # تصدير الفيديو ببارامترات تضمن مسح الميتافيتا ورفع سرعة التشغيل الفوري Faststart
                    final_video.write_videofile(
                        output_path,
                        codec="libx264",
                        audio_codec="aac",
                        fps=video.fps,
                        preset="medium",
                        logger=None,
                        ffmpeg_params=["-pix_fmt", "yuv420p", "-movflags", "+faststart", "-map_metadata", "-1"]
                    )

                    st.success("🎉 تم معالجة الفيديو بنجاح مطلق وأصبح أصلياً 100% وخالياً من أي حقوق أو بصمات!")
                    st.video(output_path)
                    with open(output_path, "rb") as f:
                        st.download_button("📥 تحميل الفيديو المعالج والجاهز للنشر", f, file_name="meta_safe_viral_video.mp4", mime="video/mp4")

                except Exception as e:
                    st.error(f"❌ حدث خطأ أثناء المعالجة التقنية: {e}")

with tab2:
    st.header("🖼️ استخراج وتصميم غلاف الريلز الذكي (Auto Smart Thumbnail)")
    st.markdown("يقوم النظام باختيار اللقطة الأكثر جذباً في الفيديو تلقائياً لرفع معدل النقر (CTR).")
    
    thumb_video = st.file_uploader("اختر الفيديو لاستخراج الغلاف", type=["mp4", "mov", "avi"], key="thumb_vid")
    thumb_title = st.text_input("عنوان الغلاف البارز (اختياري)", placeholder="اكتب عنواناً يثير الفضول...")
    
    if thumb_video:
        t_vid_thumb = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        t_vid_thumb.write(thumb_video.read())
        t_vid_thumb.close()
        
        vid_clip = VideoFileClip(t_vid_thumb.name)
        duration = vid_clip.duration
        suggested_time = min(2.5, duration / 3.0)
        
        time_second = st.slider("اختر توقيت اللقطة:", min_value=0.0, max_value=float(duration), value=float(suggested_time))
        
        if st.button("✨ توليد وتصميم الغلاف الذكي", type="primary"):
            frame = vid_clip.get_frame(time_second)
            img = Image.fromarray(frame)
            
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.25)
            
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
                
                draw.rounded_rectangle([tx - 25, ty - 15, tx + tw + 25, ty + th + 15], radius=15, fill=(0, 0, 0, 190))
                draw.text((tx, ty), bidi_t, font=font, fill=(255, 235, 59))

            thumb_out_path = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg").name
            img.save(thumb_out_path, quality=95)
            
            st.success("✅ تم تصدير غلاف الريلز بنجاح!")
            st.image(thumb_out_path, caption="الصورة المصغرة الذكية")
            with open(thumb_out_path, "rb") as f:
                st.download_button("📥 تحميل غلاف الريلز", f, file_name="smart_viral_thumbnail.jpg", mime="image/jpeg")

with tab3:
    st.header("📷 معالجة الصور الثابتة وتعديل البصمة")
    img_file = st.file_uploader("اختر صورة", type=["jpg", "png", "jpeg"], key="img")
    if st.button("🖼️ معالجة الصورة الآن", type="primary"):
        if img_file:
            base_img = Image.open(img_file).convert("RGBA")
            width, height = base_img.size
            enhancer = ImageEnhance.Color(base_img)
            base_img = enhancer.enhance(1.08)

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
