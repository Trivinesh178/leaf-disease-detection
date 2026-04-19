import streamlit as st
import requests
import os
from dotenv import load_dotenv
from deep_translator import GoogleTranslator
from streamlit_js_eval import get_geolocation

load_dotenv()

st.set_page_config(
    page_title="Leaf Disease Detection",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Language Setup ─────────────────────────────────────────────────────────────
lang_codes = {
    "English":              "en",
    "🇮🇳 हिंदी (Hindi)":    "hi",
    "🇮🇳 தமிழ் (Tamil)":    "ta",
    "🇮🇳 తెలుగు (Telugu)":   "te",
    "🇮🇳 ಕನ್ನಡ (Kannada)":  "kn",
    "🇮🇳 मराठी (Marathi)":  "mr",
    "🇮🇳 বাংলা (Bengali)":  "bn",
}

translations = {
    "Leaf Disease Detection":{"English":"Leaf Disease Detection","🇮🇳 हिंदी (Hindi)":"पत्ती रोग पहचान","🇮🇳 தமிழ் (Tamil)":"இலை நோய் கண்டறிதல்","🇮🇳 తెలుగు (Telugu)":"ఆకు వ్యాధి నిర్ధారణ","🇮🇳 ಕನ್ನಡ (Kannada)":"ಎಲೆ ರೋಗ ಪತ್ತೆ","🇮🇳 मराठी (Marathi)":"पाने रोग ओळख","🇮🇳 বাংলা (Bengali)":"পাতার রোগ সনাক্তকরণ"},
    "Upload a leaf image to detect diseases and get expert recommendations.":{"English":"Upload a leaf image to detect diseases and get expert recommendations.","🇮🇳 हिंदी (Hindi)":"रोग का पता लगाने और विशेषज्ञ सिफारिशें प्राप्त करने के लिए पत्ती की छवि अपलोड करें।","🇮🇳 தமிழ் (Tamil)":"நோய்களைக் கண்டறிந்து நிபுணர் பரிந்துரைகளைப் பெற இலை படத்தைப் பதிவேற்றவும்.","🇮🇳 తెలుగు (Telugu)":"వ్యాధులను గుర్తించడానికి మరియు నిపుణుల సిఫార్సులను పొందడానికి ఆకు చిత్రాన్ని అప్లోడ్ చేయండి.","🇮🇳 ಕನ್ನಡ (Kannada)":"ರೋಗಗಳನ್ನು ಪತ್ತೆಹಚ್ಚಲು ಮತ್ತು ತಜ್ಞರ ಶಿಫಾರಸುಗಳನ್ನು ಪಡೆಯಲು ಎಲೆ ಚಿತ್ರವನ್ನು ಅಪ್ಲೋಡ್ ಮಾಡಿ.","🇮🇳 मराठी (Marathi)":"रोग शोधण्यासाठी आणि तज्ञांच्या शिफारसी मिळवण्यासाठी पानाची प्रतिमा अपलोड करा.","🇮🇳 বাংলা (Bengali)":"রোগ সনাক্ত করতে এবং বিশেষজ্ঞ সুপারিশ পেতে একটি পাতার ছবি আপলোড করুন।"},
    "Upload Leaf Image":{"English":"Upload Leaf Image","🇮🇳 हिंदी (Hindi)":"पत्ती की छवि अपलोड करें","🇮🇳 தமிழ் (Tamil)":"இலை படத்தை பதிவேற்றவும்","🇮🇳 తెలుగు (Telugu)":"ఆకు చిత్రాన్ని అప్లోడ్ చేయండి","🇮🇳 ಕನ್ನಡ (Kannada)":"ಎಲೆ ಚಿತ್ರವನ್ನು ಅಪ್ಲೋಡ್ ಮಾಡಿ","🇮🇳 मराठी (Marathi)":"पानाची प्रतिमा अपलोड करा","🇮🇳 বাংলা (Bengali)":"পাতার ছবি আপলোড করুন"},
    "Preview":{"English":"Preview","🇮🇳 हिंदी (Hindi)":"पूर्वावलोकन","🇮🇳 தமிழ் (Tamil)":"முன்னோட்டம்","🇮🇳 తెలుగు (Telugu)":"మునుజూపు","🇮🇳 ಕನ್ನಡ (Kannada)":"ಪೂರ್ವವೀಕ್ಷಣೆ","🇮🇳 मराठी (Marathi)":"पूर्वावलोकन","🇮🇳 বাংলা (Bengali)":"প্রিভিউ"},
    "🔍 Detect Disease":{"English":"🔍 Detect Disease","🇮🇳 हिंदी (Hindi)":"🔍 रोग पहचानें","🇮🇳 தமிழ் (Tamil)":"🔍 நோயைக் கண்டறி","🇮🇳 తెలుగు (Telugu)":"🔍 వ్యాధిని గుర్తించు","🇮🇳 ಕನ್ನಡ (Kannada)":"🔍 ರೋಗವನ್ನು ಪತ್ತೆ ಮಾಡಿ","🇮🇳 मराठी (Marathi)":"🔍 रोग शोधा","🇮🇳 বাংলা (Bengali)":"🔍 রোগ সনাক্ত করুন"},
    "Analyzing image and contacting API...":{"English":"Analyzing image and contacting API...","🇮🇳 हिंदी (Hindi)":"छवि का विश्लेषण हो रहा है...","🇮🇳 தமிழ் (Tamil)":"படம் பகுப்பாய்வு செய்யப்படுகிறது...","🇮🇳 తెలుగు (Telugu)":"చిత్రాన్ని విశ్లేషిస్తోంది...","🇮🇳 ಕನ್ನಡ (Kannada)":"ಚಿತ್ರ ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ...","🇮🇳 मराठी (Marathi)":"प्रतिमा विश्लेषण केली जात आहे...","🇮🇳 বাংলা (Bengali)":"ছবি বিশ্লেষণ করা হচ্ছে..."},
    "⚠️ Invalid Image":{"English":"⚠️ Invalid Image","🇮🇳 हिंदी (Hindi)":"⚠️ अमान्य छवि","🇮🇳 தமிழ் (Tamil)":"⚠️ தவறான படம்","🇮🇳 తెలుగు (Telugu)":"⚠️ చెల్లని చిత్రం","🇮🇳 ಕನ್ನಡ (Kannada)":"⚠️ ಅಮಾನ್ಯ ಚಿತ್ರ","🇮🇳 मराठी (Marathi)":"⚠️ अवैध प्रतिमा","🇮🇳 বাংলা (Bengali)":"⚠️ অবৈধ ছবি"},
    "Please upload a clear image of a plant leaf for accurate disease detection.":{"English":"Please upload a clear image of a plant leaf for accurate disease detection.","🇮🇳 हिंदी (Hindi)":"कृपया सटीक रोग पहचान के लिए पत्ती की स्पष्ट छवि अपलोड करें।","🇮🇳 தமிழ் (Tamil)":"துல்லியமான நோய் கண்டறிதலுக்கு தயவுசெய்து இலையின் தெளிவான படத்தை பதிவேற்றவும்.","🇮🇳 తెలుగు (Telugu)":"ఖచ్చితమైన వ్యాధి నిర్ధారణ కోసం దయచేసి ఆకు యొక్క స్పష్టమైన చిత్రాన్ని అప్లోడ్ చేయండి.","🇮🇳 ಕನ್ನಡ (Kannada)":"ನಿಖರವಾದ ರೋಗ ಪತ್ತೆಗಾಗಿ ದಯವಿಟ್ಟು ಎಲೆಯ ಸ್ಪಷ್ಟ ಚಿತ್ರವನ್ನು ಅಪ್ಲೋಡ್ ಮಾಡಿ.","🇮🇳 मराठी (Marathi)":"अचूक रोग ओळखण्यासाठी कृपया पानाची स्पष्ट प्रतिमा अपलोड करा.","🇮🇳 বাংলা (Bengali)":"সঠিক রোগ সনাক্তকরণের জন্য দয়া করে একটি পাতার স্পষ্ট ছবি আপলোড করুন।"},
    "Plant":{"English":"Plant","🇮🇳 हिंदी (Hindi)":"पौधा","🇮🇳 தமிழ் (Tamil)":"செடி","🇮🇳 తెలుగు (Telugu)":"మొక్క","🇮🇳 ಕನ್ನಡ (Kannada)":"ಸಸ್ಯ","🇮🇳 मराठी (Marathi)":"झाड","🇮🇳 বাংলা (Bengali)":"গাছ"},
    "Issue":{"English":"Issue","🇮🇳 हिंदी (Hindi)":"समस्या","🇮🇳 தமிழ் (Tamil)":"சிக்கல்","🇮🇳 తెలుగు (Telugu)":"సమస్య","🇮🇳 ಕನ್ನಡ (Kannada)":"ಸಮಸ್ಯೆ","🇮🇳 मराठी (Marathi)":"समस्या","🇮🇳 বাংলা (Bengali)":"সমস্যা"},
    "What to do":{"English":"What to do","🇮🇳 हिंदी (Hindi)":"क्या करें","🇮🇳 தமிழ் (Tamil)":"என்ன செய்வது","🇮🇳 తెలుగు (Telugu)":"ఏమి చేయాలి","🇮🇳 ಕನ್ನಡ (Kannada)":"ಏನು ಮಾಡಬೇಕು","🇮🇳 मराठी (Marathi)":"काय करावे","🇮🇳 বাংলা (Bengali)":"কী করতে হবে"},
    "Type":{"English":"Type","🇮🇳 हिंदी (Hindi)":"प्रकार","🇮🇳 தமிழ் (Tamil)":"வகை","🇮🇳 తెలుగు (Telugu)":"రకం","🇮🇳 ಕನ್ನಡ (Kannada)":"ಪ್ರಕಾರ","🇮🇳 मराठी (Marathi)":"प्रकार","🇮🇳 বাংলা (Bengali)":"ধরন"},
    "Severity":{"English":"Severity","🇮🇳 हिंदी (Hindi)":"गंभीरता","🇮🇳 தமிழ் (Tamil)":"தீவிரம்","🇮🇳 తెలుగు (Telugu)":"తీవ్రత","🇮🇳 ಕನ್ನಡ (Kannada)":"ತೀವ್ರತೆ","🇮🇳 मराठी (Marathi)":"तीव्रता","🇮🇳 বাংলা (Bengali)":"তীব্রতা"},
    "Confidence":{"English":"Confidence","🇮🇳 हिंदी (Hindi)":"विश्वास स्तर","🇮🇳 தமிழ் (Tamil)":"நம்பிக்கை அளவு","🇮🇳 తెలుగు (Telugu)":"విశ్వాస స్థాయి","🇮🇳 ಕನ್ನಡ (Kannada)":"ವಿಶ್ವಾಸ ಮಟ್ಟ","🇮🇳 मराठी (Marathi)":"विश्वास पातळी","🇮🇳 বাংলা (Bengali)":"আস্থার মাত্রা"},
    "Symptoms":{"English":"Symptoms","🇮🇳 हिंदी (Hindi)":"लक्षण","🇮🇳 தமிழ் (Tamil)":"அறிகுறிகள்","🇮🇳 తెలుగు (Telugu)":"లక్షణాలు","🇮🇳 ಕನ್ನಡ (Kannada)":"ರೋಗಲಕ್ಷಣಗಳು","🇮🇳 मराठी (Marathi)":"लक्षणे","🇮🇳 বাংলা (Bengali)":"উপসর্গ"},
    "Possible Causes":{"English":"Possible Causes","🇮🇳 हिंदी (Hindi)":"संभावित कारण","🇮🇳 தமிழ் (Tamil)":"சாத்தியமான காரணங்கள்","🇮🇳 తెలుగు (Telugu)":"సాధ్యమైన కారణాలు","🇮🇳 ಕನ್ನಡ (Kannada)":"ಸಂಭವನೀಯ ಕಾರಣಗಳು","🇮🇳 मराठी (Marathi)":"संभाव्य कारणे","🇮🇳 বাংলা (Bengali)":"সম্ভাব্য কারণ"},
    "Treatment":{"English":"Treatment","🇮🇳 हिंदी (Hindi)":"उपचार","🇮🇳 தமிழ் (Tamil)":"சிகிச்சை","🇮🇳 తెలుగు (Telugu)":"చికిత్స","🇮🇳 ಕನ್ನಡ (Kannada)":"ಚಿಕಿತ್ಸೆ","🇮🇳 मराठी (Marathi)":"उपचार","🇮🇳 বাংলা (Bengali)":"চিকিৎসা"},
    "✅ Healthy Leaf":{"English":"✅ Healthy Leaf","🇮🇳 हिंदी (Hindi)":"✅ स्वस्थ पत्ती","🇮🇳 தமிழ் (Tamil)":"✅ ஆரோக்கியமான இலை","🇮🇳 తెలుగు (Telugu)":"✅ ఆరోగ్యకరమైన ఆకు","🇮🇳 ಕನ್ನಡ (Kannada)":"✅ ಆರೋಗ್ಯಕರ ಎಲೆ","🇮🇳 मराठी (Marathi)":"✅ निरोगी पान","🇮🇳 বাংলা (Bengali)":"✅ সুস্থ পাতা"},
    "No disease detected in this leaf. The plant appears to be healthy!":{"English":"No disease detected in this leaf. The plant appears to be healthy!","🇮🇳 हिंदी (Hindi)":"इस पत्ती में कोई रोग नहीं पाया गया। पौधा स्वस्थ दिखता है!","🇮🇳 தமிழ் (Tamil)":"இந்த இலையில் நோய் எதுவும் கண்டறியப்படவில்லை. செடி ஆரோக்கியமாக உள்ளது!","🇮🇳 తెలుగు (Telugu)":"ఈ ఆకులో ఏ వ్యాధి గుర్తించబడలేదు. మొక్క ఆరోగ్యంగా కనిపిస్తోంది!","🇮🇳 ಕನ್ನಡ (Kannada)":"ಈ ಎಲೆಯಲ್ಲಿ ಯಾವುದೇ ರೋಗ ಕಂಡುಬಂದಿಲ್ಲ. ಸಸ್ಯವು ಆರೋಗ್ಯಕರವಾಗಿದೆ!","🇮🇳 मराठी (Marathi)":"या पानात कोणताही रोग आढळला नाही. झाड निरोगी दिसते!","🇮🇳 বাংলা (Bengali)":"এই পাতায় কোনো রোগ সনাক্ত হয়নি। গাছটি সুস্থ দেখাচ্ছে!"},
    "Status":{"English":"Status","🇮🇳 हिंदी (Hindi)":"स्थिति","🇮🇳 தமிழ் (Tamil)":"நிலை","🇮🇳 తెలుగు (Telugu)":"స్థితి","🇮🇳 ಕನ್ನಡ (Kannada)":"ಸ್ಥಿತಿ","🇮🇳 मराठी (Marathi)":"स्थिती","🇮🇳 বাংলা (Bengali)":"অবস্থা"},
    "Cannot connect to API server. Please make sure the backend is running!":{"English":"Cannot connect to API server. Please make sure the backend is running!","🇮🇳 हिंदी (Hindi)":"API सर्वर से कनेक्ट नहीं हो सका। कृपया बैकएंड चालू करें!","🇮🇳 தமிழ் (Tamil)":"API சேவையகத்துடன் இணைக்க முடியவில்லை. பின்தள சேவை இயங்குகிறதா என சரிபார்க்கவும்!","🇮🇳 తెలుగు (Telugu)":"API సర్వర్‌కు కనెక్ట్ అవ్వడం సాధ్యం కాలేదు. బ్యాకెండ్ నడుస్తుందో తనిఖీ చేయండి!","🇮🇳 ಕನ್ನಡ (Kannada)":"API ಸರ್ವರ್‌ಗೆ ಸಂಪರ್ಕಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ. ಬ್ಯಾಕೆಂಡ್ ಚಾಲನೆಯಲ್ಲಿದೆಯೇ ಎಂದು ಪರಿಶೀಲಿಸಿ!","🇮🇳 मराठी (Marathi)":"API सर्व्हरशी कनेक्ट करता आले नाही. बॅकएंड सुरू आहे का ते तपासा!","🇮🇳 বাংলা (Bengali)":"API সার্ভারে সংযোগ করা যাচ্ছে না। ব্যাকএন্ড চালু আছে কিনা নিশ্চিত করুন!"},
    "Request timed out. The API might be processing a large image or is slow to respond.":{"English":"Request timed out. The API might be processing a large image or is slow to respond.","🇮🇳 हिंदी (Hindi)":"अनुरोध का समय समाप्त हो गया। API धीमी हो सकती है।","🇮🇳 தமிழ் (Tamil)":"கோரிக்கை நேர முடிவடைந்தது. API மெதுவாக பதிலளிக்கலாம்.","🇮🇳 తెలుగు (Telugu)":"అభ్యర్థన సమయం ముగిసింది. API నెమ్మదిగా స్పందిస్తోంది.","🇮🇳 ಕನ್ನಡ (Kannada)":"ವಿನಂತಿ ಸಮಯ ಮೀರಿತು. API ನಿಧಾನವಾಗಿ ಪ್ರತಿಕ್ರಿಯಿಸುತ್ತಿರಬಹುದು.","🇮🇳 मराठी (Marathi)":"विनंती वेळ संपली. API हळू असू शकते.","🇮🇳 বাংলা (Bengali)":"অনুরোধের সময় শেষ হয়ে গেছে। API ধীরে সাড়া দিতে পারে।"},
    "Expert Recommendation":{"English":"Expert Recommendation","🇮🇳 हिंदी (Hindi)":"विशेषज्ञ सिफारिश","🇮🇳 தமிழ் (Tamil)":"நிபுணர் பரிந்துரை","🇮🇳 తెలుగు (Telugu)":"నిపుణుల సిఫార్సు","🇮🇳 ಕನ್ನಡ (Kannada)":"ತಜ್ಞರ ಶಿಫಾರಸು","🇮🇳 मराठी (Marathi)":"तज्ञांची शिफारस","🇮🇳 বাংলা (Bengali)":"বিশেষজ্ঞ পরামর্শ"},
    "Run: python run_backend.py in a separate terminal":{"English":"Run: python run_backend.py in a separate terminal","🇮🇳 हिंदी (Hindi)":"अलग टर्मिनल में चलाएं: python run_backend.py","🇮🇳 தமிழ் (Tamil)":"தனி டெர்மினலில் இயக்கவும்: python run_backend.py","🇮🇳 తెలుగు (Telugu)":"వేరే టెర్మినల్‌లో అమలు చేయండి: python run_backend.py","🇮🇳 ಕನ್ನಡ (Kannada)":"ಪ್ರತ್ಯೇಕ ಟರ್ಮಿನಲ್‌ನಲ್ಲಿ ರನ್ ಮಾಡಿ: python run_backend.py","🇮🇳 मराठी (Marathi)":"वेगळ्या टर्मिनलमध्ये चालवा: python run_backend.py","🇮🇳 বাংলা (Bengali)":"আলাদা টার্মিনালে চালান: python run_backend.py"},
    "🚨 Act within 48 hours":{"English":"🚨 Act within 48 hours","🇮🇳 हिंदी (Hindi)":"🚨 48 घंटों के भीतर कार्रवाई करें","🇮🇳 தமிழ் (Tamil)":"🚨 48 மணி நேரத்திற்குள் நடவடிக்கை எடுக்கவும்","🇮🇳 తెలుగు (Telugu)":"🚨 48 గంటల్లో చర్య తీసుకోండి","🇮🇳 ಕನ್ನಡ (Kannada)":"🚨 48 ಗಂಟೆಗಳಲ್ಲಿ ಕ್ರಮ ತೆಗೆಡಿ","🇮🇳 मराठी (Marathi)":"🚨 ४८ तासांत कारवाई करा","🇮🇳 বাংলা (Bengali)":"🚨 ৪৮ ঘণ্টার মধ্যে ব্যবস্থা নিন"},
    "⚠️ Act within a week":{"English":"⚠️ Act within a week","🇮🇳 हिंदी (Hindi)":"⚠️ एक सप्ताह के भीतर कार्रवाई करें","🇮🇳 தமிழ் (Tamil)":"⚠️ ஒரு வாரத்திற்குள் நடவடிக்கை எடுக்கவும்","🇮🇳 తెలుగు (Telugu)":"⚠️ ఒక వారంలో చర్య తీసుకోండి","🇮🇳 ಕನ್ನಡ (Kannada)":"⚠️ ಒಂದು ವಾರದಲ್ಲಿ ಕ್ರಮ ತೆಗೆಡಿ","🇮🇳 मराठी (Marathi)":"⚠️ एका आठवड्यात कारवाई करा","🇮🇳 বাংলা (Bengali)":"⚠️ এক সপ্তাহের মধ্যে ব্যবস্থা নিন"},
    "✅ Can wait — monitor closely":{"English":"✅ Can wait — monitor closely","🇮🇳 हिंदी (Hindi)":"✅ प्रतीक्षा कर सकते हैं — ध्यान से देखें","🇮🇳 தமிழ் (Tamil)":"✅ காத்திருக்கலாம் — கவனமாகக் கண்காணிக்கவும்","🇮🇳 తెలుగు (Telugu)":"✅ వేచి ఉండవచ్చు — జాగ్రత్తగా గమనించండి","🇮🇳 ಕನ್ನಡ (Kannada)":"✅ ಕಾಯಬಹುದು — ಎಚ್ಚರಿಕೆಯಿಂದ ಗಮನಿಸಿ","🇮🇳 मराठी (Marathi)":"✅ थांबू शकतो — काळजीपूर्वक निरीक्षण करा","🇮🇳 বাংলা (Bengali)":"✅ অপেক্ষা করা যাবে — মনোযোগ দিয়ে পর্যবেক্ষণ করুন"},
    "Leaf Health":{"English":"Leaf Health","🇮🇳 हिंदी (Hindi)":"पत्ती का स्वास्थ्य","🇮🇳 தமிழ் (Tamil)":"இலை ஆரோக்கியம்","🇮🇳 తెలుగు (Telugu)":"ఆకు ఆరోగ్యం","🇮🇳 ಕನ್ನಡ (Kannada)":"ಎಲೆ ಆರೋಗ್ಯ","🇮🇳 मराठी (Marathi)":"पानाचे आरोग्य","🇮🇳 বাংলা (Bengali)":"পাতার স্বাস্থ্য"},
    "Leaf Health Score":{"English":"Leaf Health Score","🇮🇳 हिंदी (Hindi)":"पत्ती स्वास्थ्य स्कोर","🇮🇳 தமிழ் (Tamil)":"இலை ஆரோக்கிய மதிப்பெண்","🇮🇳 తెలుగు (Telugu)":"ఆకు ఆరోగ్య స్కోర్","🇮🇳 ಕನ್ನಡ (Kannada)":"ಎಲೆ ಆರೋಗ್ಯ ಅಂಕ","🇮🇳 मराठी (Marathi)":"पानाचे आरोग्य गुण","🇮🇳 বাংলা (Bengali)":"পাতার স্বাস্থ্য স্কোর"},
    "Healthy":{"English":"Healthy","🇮🇳 हिंदी (Hindi)":"स्वस्थ","🇮🇳 தமிழ் (Tamil)":"ஆரோக்கியமான","🇮🇳 తెలుగు (Telugu)":"ఆరోగ్యకర","🇮🇳 ಕನ್ನಡ (Kannada)":"ಆರೋಗ್ಯಕರ","🇮🇳 मराठी (Marathi)":"निरोगी","🇮🇳 বাংলা (Bengali)":"সুস্থ"},
    "At Risk":{"English":"At Risk","🇮🇳 हिंदी (Hindi)":"जोखिम में","🇮🇳 தமிழ் (Tamil)":"ஆபத்தில்","🇮🇳 తెలుగు (Telugu)":"ప్రమాదంలో","🇮🇳 ಕನ್ನಡ (Kannada)":"ಅಪಾಯದಲ್ಲಿ","🇮🇳 मराठी (Marathi)":"धोक्यात","🇮🇳 বাংলা (Bengali)":"ঝুঁকিতে"},
    "Diseased":{"English":"Diseased","🇮🇳 हिंदी (Hindi)":"रोगग्रस्त","🇮🇳 தமிழ் (Tamil)":"நோய்வாய்ப்பட்ட","🇮🇳 తెలుగు (Telugu)":"వ్యాధిగ్రస్తమైన","🇮🇳 ಕನ್ನಡ (Kannada)":"ರೋಗಪೀಡಿತ","🇮🇳 मराठी (Marathi)":"रोगग्रस्त","🇮🇳 বাংলা (Bengali)":"রোগাক্রান্ত"},
    "🛡️ Prevention":{"English":"🛡️ Prevention","🇮🇳 हिंदी (Hindi)":"🛡️ बचाव","🇮🇳 தமிழ் (Tamil)":"🛡️ தடுப்பு","🇮🇳 తెలుగు (Telugu)":"🛡️ నివారణ","🇮🇳 ಕನ್ನಡ (Kannada)":"🛡️ ತಡೆಗಟ್ಟುವಿಕೆ","🇮🇳 मराठी (Marathi)":"🛡️ प्रतिबंध","🇮🇳 বাংলা (Bengali)":"🛡️ প্রতিরোধ"},
    "Affected Area":{"English":"Affected Area","🇮🇳 हिंदी (Hindi)":"प्रभावित क्षेत्र","🇮🇳 தமிழ் (Tamil)":"பாதிக்கப்பட்ட பகுதி","🇮🇳 తెలుగు (Telugu)":"ప్రభావిత ప్రాంతం","🇮🇳 ಕನ್ನಡ (Kannada)":"ಪ್ರಭಾವಿತ ಪ್ರದೇಶ","🇮🇳 मराठी (Marathi)":"प्रभावित क्षेत्र","🇮🇳 বাংলা (Bengali)":"আক্রান্ত এলাকা"},
    "Spread Risk":{"English":"Spread Risk","🇮🇳 हिंदी (Hindi)":"फैलने का जोखिम","🇮🇳 தமிழ் (Tamil)":"பரவல் அபாயம்","🇮🇳 తెలుగు (Telugu)":"వ్యాప్తి ప్రమాదం","🇮🇳 ಕನ್ನಡ (Kannada)":"ಹರಡುವ ಅಪಾಯ","🇮🇳 मराठी (Marathi)":"पसरण्याचा धोका","🇮🇳 বাংলা (Bengali)":"ছড়ানোর ঝুঁকি"},
    "0–40 Diseased":{"English":"0–40 Diseased","🇮🇳 हिंदी (Hindi)":"0–40 रोगग्रस्त","🇮🇳 தமிழ் (Tamil)":"0–40 நோய்வாய்ப்பட்ட","🇮🇳 తెలుగు (Telugu)":"0–40 వ్యాధిగ్రస్త","🇮🇳 ಕನ್ನಡ (Kannada)":"0–40 ರೋಗಪೀಡಿತ","🇮🇳 मराठी (Marathi)":"0–40 रोगग्रस्त","🇮🇳 বাংলা (Bengali)":"0–40 রোগাক্রান্ত"},
    "40–70 At Risk":{"English":"40–70 At Risk","🇮🇳 हिंदी (Hindi)":"40–70 जोखिम में","🇮🇳 தமிழ் (Tamil)":"40–70 ஆபத்தில்","🇮🇳 తెలుగు (Telugu)":"40–70 ప్రమాదంలో","🇮🇳 ಕನ್ನಡ (Kannada)":"40–70 ಅಪಾಯದಲ್ಲಿ","🇮🇳 मराठी (Marathi)":"40–70 धोक्यात","🇮🇳 বাংলা (Bengali)":"40–70 ঝুঁকিতে"},
    "70–100 Healthy":{"English":"70–100 Healthy","🇮🇳 हिंदी (Hindi)":"70–100 स्वस्थ","🇮🇳 தமிழ் (Tamil)":"70–100 ஆரோக்கியமான","🇮🇳 తెలుగు (Telugu)":"70–100 ఆరోగ్యకర","🇮🇳 ಕನ್ನಡ (Kannada)":"70–100 ಆರೋಗ್ಯಕರ","🇮🇳 मराठी (Marathi)":"70–100 निरोगी","🇮🇳 বাংলা (Bengali)":"70–100 সুস্থ"},
    "✅ Plant is healthy — no action needed":{"English":"✅ Plant is healthy — no action needed","🇮🇳 हिंदी (Hindi)":"✅ पौधा स्वस्थ है — कोई कार्रवाई आवश्यक नहीं","🇮🇳 தமிழ் (Tamil)":"✅ செடி ஆரோக்கியமாக உள்ளது — நடவடிக்கை தேவையில்லை","🇮🇳 తెలుగు (Telugu)":"✅ మొక్క ఆరోగ్యంగా ఉంది — చర్య అవసరం లేదు","🇮🇳 ಕನ್ನಡ (Kannada)":"✅ ಸಸ್ಯ ಆರೋಗ್ಯಕರವಾಗಿದೆ — ಯಾವುದೇ ಕ್ರಮ ಬೇಡ","🇮🇳 मराठी (Marathi)":"✅ झाड निरोगी आहे — कोणतीही कारवाई आवश्यक नाही","🇮🇳 বাংলা (Bengali)":"✅ গাছ সুস্থ — কোনো ব্যবস্থা দরকার নেই"},
}

# ── GPS Location + Language Detection ─────────────────────────────────────────
def get_language_from_state(state: str) -> str:
    state_to_lang = {
        "Uttar Pradesh":  "🇮🇳 हिंदी (Hindi)",
        "Bihar":          "🇮🇳 हिंदी (Hindi)",
        "Rajasthan":      "🇮🇳 हिंदी (Hindi)",
        "Madhya Pradesh": "🇮🇳 हिंदी (Hindi)",
        "Haryana":        "🇮🇳 हिंदी (Hindi)",
        "Delhi":          "🇮🇳 हिंदी (Hindi)",
        "Uttarakhand":    "🇮🇳 हिंदी (Hindi)",
        "Tamil Nadu":     "🇮🇳 தமிழ் (Tamil)",
        "Andhra Pradesh": "🇮🇳 తెలుగు (Telugu)",
        "Telangana":      "🇮🇳 తెలుగు (Telugu)",
        "Karnataka":      "🇮🇳 ಕನ್ನಡ (Kannada)",
        "Maharashtra":    "🇮🇳 मराठी (Marathi)",
        "West Bengal":    "🇮🇳 বাংলা (Bengali)",
    }
    return state_to_lang.get(state, "English")

# ── Session State ──────────────────────────────────────────────────────────────
if 'selected_lang'    not in st.session_state: st.session_state.selected_lang    = "English"
if 'gps_lat'          not in st.session_state: st.session_state.gps_lat          = None
if 'gps_lon'          not in st.session_state: st.session_state.gps_lon          = None
if 'gps_state'        not in st.session_state: st.session_state.gps_state        = None
if 'gps_city'         not in st.session_state: st.session_state.gps_city         = None
if 'gps_district'     not in st.session_state: st.session_state.gps_district     = None
if 'gps_country'      not in st.session_state: st.session_state.gps_country      = None
if 'gps_pincode'      not in st.session_state: st.session_state.gps_pincode      = None
if 'location_fetched' not in st.session_state: st.session_state.location_fetched = False
# FIX: tracks whether user has manually changed language after GPS auto-set.
# When True, GPS will never overwrite the language again.
if 'lang_user_chosen'   not in st.session_state: st.session_state.lang_user_chosen   = False
if 'disease_result'    not in st.session_state: st.session_state.disease_result    = None   # cached JSON result
if 'result_file_name'  not in st.session_state: st.session_state.result_file_name  = None   # which file was analysed
if 'uploaded_bytes'    not in st.session_state: st.session_state.uploaded_bytes    = None   # cached image bytes
if 'uploaded_name'     not in st.session_state: st.session_state.uploaded_name     = None   # cached image filename
# ── Translation Engine ─────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def cached_google_translate(text: str, target_code: str) -> str:
    try:
        if target_code == "en" or not text:
            return text
        text = str(text).strip()
        MAX_CHARS = 4500
        if len(text) <= MAX_CHARS:
            return GoogleTranslator(source="en", target=target_code).translate(text)
        import re
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks, current = [], ""
        for s in sentences:
            if len(current) + len(s) + 1 <= MAX_CHARS:
                current += (" " if current else "") + s
            else:
                if current: chunks.append(current)
                current = s
        if current: chunks.append(current)
        return " ".join([GoogleTranslator(source="en", target=target_code).translate(c) for c in chunks])
    except Exception:
        return text

def translate(text):
    if not text: return text
    if text in translations:
        return translations[text].get(st.session_state.selected_lang, text)
    code = lang_codes.get(st.session_state.selected_lang, "en")
    if code == "en": return text
    try:
        r = cached_google_translate(str(text).strip(), code)
        return r if r and r.strip() else text
    except: return text

def translate_grok(text):
    if not text: return text
    code = lang_codes.get(st.session_state.selected_lang, "en")
    if code == "en": return text
    try:
        r = cached_google_translate(str(text).strip(), code)
        return r if r and r.strip() else text
    except: return text

def translate_grok_list(items):
    code = lang_codes.get(st.session_state.selected_lang, "en")
    if code == "en" or not items: return items
    out = []
    for item in items:
        try:
            t = cached_google_translate(str(item).strip(), code)
            out.append(t if t and t.strip() else item)
        except: out.append(item)
    return out

# ── Severity / Urgency Helpers ─────────────────────────────────────────────────
def severity_theme(severity: str, disease_detected: bool) -> dict:
    s = (severity or "").lower()
    if not disease_detected:
        return dict(border="#2e7d32", bg="linear-gradient(135deg,#f1f8e9,#ffffff)",
                    accent="#2e7d32", badge_bg="#e8f5e9", title_color="#2e7d32",
                    bar_color="#43a047", glow="rgba(46,125,50,0.15)", gauge_color="#43a047")
    if s == "severe":
        return dict(border="#c62828", bg="linear-gradient(135deg,#fff5f5,#ffffff)",
                    accent="#c62828", badge_bg="#ffebee", title_color="#b71c1c",
                    bar_color="#e53935", glow="rgba(198,40,40,0.18)", gauge_color="#e53935")
    if s == "moderate":
        return dict(border="#e65100", bg="linear-gradient(135deg,#fff8f0,#ffffff)",
                    accent="#e65100", badge_bg="#fff3e0", title_color="#bf360c",
                    bar_color="#fb8c00", glow="rgba(230,81,0,0.15)", gauge_color="#fb8c00")
    return dict(border="#558b2f", bg="linear-gradient(135deg,#f9fbe7,#ffffff)",
                accent="#558b2f", badge_bg="#f1f8e9", title_color="#33691e",
                bar_color="#7cb342", glow="rgba(85,139,47,0.15)", gauge_color="#7cb342")

def calc_health_score(confidence: float, severity: str, disease_detected: bool) -> int:
    """Same formula as the gauge ring — single source of truth."""
    conf = max(0, min(100, float(confidence)))
    sev  = (severity or "").lower()
    if not disease_detected:    return int(conf)
    if sev == "severe":         return max(5,  round(100 - conf * 0.9))
    if sev == "moderate":       return max(10, round(100 - conf * 0.7))
    return                             max(20, round(100 - conf * 0.4))  # mild

def urgency_key(severity, disease_detected, health_score=None):
    """
    Urgency is decided by the leaf health score shown in the gauge:
      0 – 40  → Act within 48 hours  (red)
      41 – 70 → Act within a week    (orange)
      71 – 100→ Can wait, monitor    (green)
    Healthy leaf → no action needed.
    """
    if not disease_detected:
        return "✅ Plant is healthy — no action needed"
    if health_score is not None:
        if health_score <= 40:  return "🚨 Act within 48 hours"
        if health_score <= 70:  return "⚠️ Act within a week"
        return "✅ Can wait — monitor closely"
    # Fallback to severity if health_score not passed
    s = (severity or "").lower()
    if s == "severe":   return "🚨 Act within 48 hours"
    if s == "moderate": return "⚠️ Act within a week"
    return "✅ Can wait — monitor closely"

def urgency_style(severity, disease_detected, health_score=None):
    if not disease_detected:
        return "background:#e8f5e9;color:#2e7d32;border:2px solid #a5d6a7;"
    if health_score is not None:
        if health_score <= 40:  return "background:#ffebee;color:#c62828;border:2px solid #ef9a9a;"
        if health_score <= 70:  return "background:#fff3e0;color:#e65100;border:2px solid #ffcc80;"
        return "background:#f1f8e9;color:#33691e;border:2px solid #c5e1a5;"
    s = (severity or "").lower()
    if s == "severe":   return "background:#ffebee;color:#c62828;border:2px solid #ef9a9a;"
    if s == "moderate": return "background:#fff3e0;color:#e65100;border:2px solid #ffcc80;"
    return "background:#f1f8e9;color:#33691e;border:2px solid #c5e1a5;"


def confidence_gauge_html(confidence: float, color: str, label: str,
                           disease_detected: bool = False, severity: str = "",
                           t_leaf_health: str = "Leaf Health",
                           t_leaf_score: str = "Leaf Health Score",
                           t_healthy: str = "Healthy", t_at_risk: str = "At Risk",
                           t_diseased: str = "Diseased",
                           t_zone0: str = "0–40 Diseased", t_zone1: str = "40–70 At Risk",
                           t_zone2: str = "70–100 Healthy") -> str:
    """
    Leaf Health Bar — shows how healthy the leaf is.
    Healthy leaf  → high green bar
    Moderate sick → mid orange bar
    Severe sick   → low red bar
    """
    conf = max(0, min(100, float(confidence)))
    sev  = (severity or "").lower()

    # ── Calculate leaf health score ──────────────────────────────────────
    if not disease_detected:
        # Healthy: health mirrors confidence (95% sure healthy → 95% health)
        health = conf
    elif sev == "severe":
        health = max(5,  round(100 - conf * 0.9))   # 90% conf severe → ~19% health
    elif sev == "moderate":
        health = max(10, round(100 - conf * 0.7))   # 80% conf moderate → ~44% health
    else:  # mild
        health = max(20, round(100 - conf * 0.4))   # 75% conf mild → ~70% health

    # ── Colour + label based on health score ────────────────────────────
    if health >= 70:
        bar_color   = "#43a047"
        track_color = "#c8e6c9"
        status_icon = "🟢"
        status_text = "Healthy"
        status_bg   = "#e8f5e9"
        status_fg   = "#1b5e20"
    elif health >= 40:
        bar_color   = "#fb8c00"
        track_color = "#ffe0b2"
        status_icon = "🟡"
        status_text = "At Risk"
        status_bg   = "#fff3e0"
        status_fg   = "#bf360c"
    else:
        bar_color   = "#e53935"
        track_color = "#ffcdd2"
        status_icon = "🔴"
        status_text = f"{t_diseased}"
        status_bg   = "#ffebee"
        status_fg   = "#b71c1c"

    # SVG ring for health
    radius      = 52
    circ        = 2 * 3.14159 * radius
    dash        = circ * health / 100
    gap         = circ - dash

    # Leaf icon path (simple teardrop-like shape)
    leaf_path = "M12,2 C7,2 2,7 2,12 C2,17 7,22 12,22 C17,22 22,17 22,12 C22,7 17,2 12,2 Z"

    return f"""

    <div style="margin:16px 0 12px 0;animation:leafFadeUp 0.5s ease both;">
      <div style="font-size:1em;font-weight:700;color:#388e3c;margin-bottom:12px;
                  display:flex;align-items:center;gap:6px;">
        🌿 {t_leaf_health}
      </div>

      <div style="display:flex;align-items:center;gap:22px;flex-wrap:wrap;">
        <div style="position:relative;width:130px;height:130px;flex-shrink:0;">
          <svg width="130" height="130" viewBox="0 0 130 130"
               style="transform:rotate(-90deg);">
            <circle cx="65" cy="65" r="{radius}" fill="none"
              stroke="{track_color}" stroke-width="13"/>
            <circle cx="65" cy="65" r="{radius}" fill="none"
              stroke="{bar_color}" stroke-width="13" stroke-linecap="round"
              stroke-dasharray="0 {circ:.1f}"
              style="animation:leafRingAnim 1.4s cubic-bezier(.4,0,.2,1) forwards;--leaf-dash:{dash:.1f};"/>
          </svg>
          <div style="position:absolute;top:50%;left:50%;
                      transform:translate(-50%,-50%);text-align:center;line-height:1.15;">
            <div style="font-size:1.1em;">🍃</div>
            <div style="font-size:1.7em;font-weight:800;color:{bar_color};
                        letter-spacing:-1px;margin-top:2px;">
              {health:.0f}<span style="font-size:0.42em;font-weight:600;">%</span>
            </div>
          </div>
        </div>
        <div style="flex:1;min-width:170px;">
          <div style="display:inline-flex;align-items:center;gap:7px;
                      background:{status_bg};border:2px solid {bar_color}44;
                      border-radius:14px;padding:0.45em 1.1em;margin-bottom:14px;">
            <span style="font-size:1em;">{status_icon}</span>
            <span style="font-weight:800;color:{status_fg};font-size:1em;">
              {status_text}
            </span>
          </div>
          <div style="font-size:0.82em;color:#757575;font-weight:600;margin-bottom:6px;">
            {t_leaf_score}
          </div>
          <div style="background:{track_color};border-radius:99px;height:20px;
                      overflow:hidden;box-shadow:inset 0 1px 4px rgba(0,0,0,0.08);">
            <div style="height:100%;width:0%;
                        background:linear-gradient(90deg,{bar_color}99,{bar_color});
                        border-radius:99px;
                        animation:leafBarAnim 1.4s cubic-bezier(.4,0,.2,1) forwards;--leaf-bar-w:{health:.0f}%;">
            </div>
          </div>
          <div style="display:flex;justify-content:space-between;
                      font-size:0.73em;color:#9e9e9e;margin-top:4px;">
            <span>💀 0</span><span>50</span><span>🌿 100</span>
          </div>
          <div style="display:flex;gap:6px;margin-top:10px;flex-wrap:wrap;">
            <span style="font-size:0.72em;font-weight:600;color:#e53935;
                         background:#ffebee;border-radius:8px;padding:2px 8px;">
              🔴 {t_zone0}
            </span>
            <span style="font-size:0.72em;font-weight:600;color:#e65100;
                         background:#fff3e0;border-radius:8px;padding:2px 8px;">
              🟡 {t_zone1}
            </span>
            <span style="font-size:0.72em;font-weight:600;color:#2e7d32;
                         background:#e8f5e9;border-radius:8px;padding:2px 8px;">
              🟢 {t_zone2}
            </span></div></div></div></div><span style="display:none"></span>
    
    """

# ── GPS Location via Browser ───────────────────────────────────────────────────
if not st.session_state.location_fetched:
    loc = get_geolocation()
    if loc is not None:
        try:
            lat = loc["coords"]["latitude"]
            lon = loc["coords"]["longitude"]

            # Store exact GPS coordinates (ready for future weather API calls)
            st.session_state.gps_lat = round(lat, 6)
            st.session_state.gps_lon = round(lon, 6)

            # Reverse geocode with full addressdetails
            geo = requests.get(
                f"https://nominatim.openstreetmap.org/reverse"
                f"?lat={lat}&lon={lon}&format=json&addressdetails=1",
                headers={"User-Agent": "LeafDiseaseApp/1.0"},
                timeout=5
            ).json()

            address  = geo.get("address", {})

            # State — strip redundant suffix (e.g. "Telangana State" → "Telangana")
            state    = address.get("state", "").replace(" State", "")

            # City — try multiple Nominatim fields in priority order
            city     = (address.get("city")
                     or address.get("town")
                     or address.get("village")
                     or address.get("suburb", ""))

            # District — Nominatim uses "county" for Indian districts
            # For Telangana/AP: "state_district" = actual district (e.g. "Hyderabad", "Medchal-Malkajgiri")
            # "county" = mandal level in some states — skip it
            # Priority: state_district → county → district → municipality
            # Strip " District" suffix if present (e.g. "Hyderabad District" → "Hyderabad")
            district = (
                address.get("state_district") or
                address.get("county") or
                address.get("district") or
                address.get("municipality") or ""
            ).replace(" District", "").replace(" Mandal", "").strip()

            # Country and pincode
            country  = address.get("country", "")
            pincode  = address.get("postcode", "")

            # Save all location fields to session state
            st.session_state.gps_state    = state
            st.session_state.gps_city     = city
            st.session_state.gps_district = district
            st.session_state.gps_country  = country
            st.session_state.gps_pincode  = pincode

            # Auto-set UI language based on detected state ONLY on first GPS fetch.
            # If user already manually picked a language, don't overwrite it.
            if not st.session_state.lang_user_chosen:
                st.session_state.selected_lang = get_language_from_state(state)

        except Exception:
            pass
        st.session_state.location_fetched = True
        st.rerun()

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""<style>
/* ── Page background ── */
.stApp {
  background: linear-gradient(160deg, #e8f5e9 0%, #e3f2fd 50%, #f3e5f5 100%);
  min-height: 100vh;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer { visibility: hidden; }
[data-testid="stHeader"] { background: transparent; }

/* ── Language selector pill ── */
[data-testid="stSelectbox"] > div > div {
  border-radius: 99px !important;
}

/* ── Upload button ── */
[data-testid="stFileUploaderDropzone"] {
  border: 2px solid #81c784 !important;
  border-radius: 16px !important;
  background: rgba(255,255,255,0.7) !important;
  transition: border-color 0.2s, background 0.2s;
}
[data-testid="stFileUploaderDropzone"]:hover {
  border-color: #388e3c !important;
  background: rgba(232,245,233,0.9) !important;
}

/* ── Detect button ── */
[data-testid="stBaseButton-secondary"],
button[kind="secondary"] {
  border-radius: 14px !important;
  font-size: 1.1rem !important;
  font-weight: 700 !important;
  padding: 0.7rem 1.5rem !important;
  border: 2px solid #2e7d32 !important;
  color: #2e7d32 !important;
  background: white !important;
  transition: all 0.2s !important;
}
[data-testid="stBaseButton-secondary"]:hover,
button[kind="secondary"]:hover {
  background: #2e7d32 !important;
  color: white !important;
}

/* ── Result card ── */
.result-card {
  border-radius: 22px;
  padding: 2.2em 2em 1.8em 2em;
  margin-top: 0.5em;
  margin-bottom: 1em;
  transition: box-shadow 0.3s;
}
.result-card:hover { box-shadow: 0 12px 40px rgba(0,0,0,0.12) !important; }

/* ── Section titles ── */
.section-title {
  font-size: 1.1em; font-weight: 700; margin-top: 1.3em;
  margin-bottom: 0.4em; letter-spacing: 0.3px;
  display: flex; align-items: center; gap: 6px;
}

/* ── Lists ── */
.sym-list, .cause-list, .treat-list {
  margin: 0.3em 0 0.3em 1.2em; line-height: 2;
}
.sym-list li::marker   { color: #ef5350; }
.cause-list li::marker { color: #fb8c00; }
.treat-list li::marker { color: #43a047; }

/* ── Info chips ── */
.chip {
  display: inline-flex; align-items: center; gap: 5px;
  border-radius: 99px; padding: 0.28em 0.9em;
  font-size: 0.92em; font-weight: 600;
  margin-right: 6px; margin-bottom: 6px;
}

/* ── Urgency banner ── */
.urgency {
  display: inline-block; border-radius: 12px;
  padding: 0.5em 1.3em; font-size: 1.05em; font-weight: 800;
  margin: 0.6em 0 0.9em 0; letter-spacing: 0.2px;
}

/* ── Timestamp ── */
.ts { color: #bdbdbd; font-size: 0.82em; text-align: right; margin-top: 1.4em; }

/* ── Left panel card ── */
.upload-panel {
  background: rgba(255,255,255,0.75);
  backdrop-filter: blur(8px);
  border-radius: 20px;
  padding: 1.4em 1.2em;
  box-shadow: 0 2px 16px rgba(0,0,0,0.07);
  border: 1px solid rgba(255,255,255,0.9);
}

/* ── Hero header ── */
.hero-wrap {
  text-align: center;
  padding: 2.2em 1em 1.6em 1em;
  background: rgba(255,255,255,0.55);
  backdrop-filter: blur(10px);
  border-radius: 24px;
  margin-bottom: 2em;
  box-shadow: 0 2px 20px rgba(46,125,50,0.08);
  border: 1px solid rgba(255,255,255,0.8);
}

@keyframes leafRingAnim {
  from { stroke-dasharray: 0 500; }
  to   { stroke-dasharray: var(--leaf-dash) 500; }
}
@keyframes leafBarAnim {
  from { width: 0%; }
  to   { width: var(--leaf-bar-w); }
}
@keyframes leafFadeUp {
  from { opacity:0; transform:translateY(6px); }
  to   { opacity:1; transform:translateY(0); }
}
</style>""", unsafe_allow_html=True)

# ── Top language selector ──────────────────────────────────────────────────────
_, loc_col, lang_col = st.columns([4, 2, 1])

# Show location pill — short label visible always, full card on hover
with loc_col:
    if st.session_state.get("gps_state"):
        _city     = st.session_state.get("gps_city", "")
        _district = st.session_state.get("gps_district", "")
        _state    = st.session_state.get("gps_state", "")
        _country  = st.session_state.get("gps_country", "")
        _pincode  = st.session_state.get("gps_pincode", "")
        _lat      = st.session_state.get("gps_lat")
        _lon      = st.session_state.get("gps_lon")

        # Short label shown always: City, State
        _short = ", ".join(p for p in [_district, _state] if p)

        # Full detail shown on hover
        _coord_str = f"{_lat:.6f}°N, {_lon:.6f}°E" if _lat and _lon else ""

        # Build hover rows — only non-empty fields
        _hover_rows = ""
        if _city:
            _hover_rows += f"<div class='loc-row'><span class='loc-icon'>🏙️</span><span>{_city}</span></div>"
        if _district:
            _hover_rows += f"<div class='loc-row'><span class='loc-icon'>🗺️</span><span>{_district}</span></div>"
        if _state:
            _hover_rows += f"<div class='loc-row'><span class='loc-icon'>📌</span><span>{_state}</span></div>"
        if _country:
            _hover_rows += f"<div class='loc-row'><span class='loc-icon'>🌏</span><span>{_country}</span></div>"
        if _pincode:
            _hover_rows += f"<div class='loc-row'><span class='loc-icon'>📮</span><span>{_pincode}</span></div>"
        if _coord_str:
            _hover_rows += f"<div class='loc-row'><span class='loc-icon'>🛰️</span><span style='font-family:monospace;font-size:0.85em;'>{_coord_str}</span></div>"

        st.markdown(f"""
        <style>
        .loc-wrapper {{
            position: relative;
            display: inline-flex;
            justify-content: flex-end;
            width: 100%;
            padding-top: 0.3em;
        }}
        .loc-pill {{
            display: inline-flex;
            align-items: center;
            gap: 5px;
            background: linear-gradient(135deg,#e8f5e9,#f1f8e9);
            border: 1.5px solid #a5d6a7;
            border-radius: 99px;
            padding: 0.28em 0.85em;
            font-size: 0.82em;
            font-weight: 700;
            color: #2e7d32;
            cursor: default;
            user-select: none;
            white-space: nowrap;
            box-shadow: 0 1px 4px rgba(46,125,50,0.10);
            transition: box-shadow 0.2s, border-color 0.2s;
        }}
        .loc-pill:hover {{
            border-color: #66bb6a;
            box-shadow: 0 2px 10px rgba(46,125,50,0.18);
        }}
        .loc-card {{
            display: none;
            position: absolute;
            top: calc(100% + 8px);
            right: 0;
            z-index: 9999;
            background: #ffffff;
            border: 1.5px solid #c8e6c9;
            border-radius: 16px;
            padding: 1em 1.2em;
            min-width: 220px;
            box-shadow: 0 8px 32px rgba(46,125,50,0.15), 0 2px 8px rgba(0,0,0,0.08);
            animation: locFadeIn 0.18s ease both;
        }}
        .loc-wrapper:hover .loc-card {{
            display: block;
        }}
        .loc-card-title {{
            font-size: 0.78em;
            font-weight: 800;
            color: #1b5e20;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 0.65em;
            padding-bottom: 0.45em;
            border-bottom: 1.5px solid #e8f5e9;
        }}
        .loc-row {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.88em;
            color: #2e7d32;
            font-weight: 600;
            padding: 0.22em 0;
        }}
        .loc-icon {{
            font-size: 1em;
            width: 20px;
            text-align: center;
            flex-shrink: 0;
        }}
        @keyframes locFadeIn {{
            from {{ opacity:0; transform:translateY(-4px); }}
            to   {{ opacity:1; transform:translateY(0); }}
        }}
        </style>

        <div class="loc-wrapper">
          <div class="loc-pill">
            📍 {_short}
          </div>
          <div class="loc-card">
            <div class="loc-card-title">📍 Your Location</div>
            {_hover_rows}
          </div>
        </div>
        """, unsafe_allow_html=True)

with lang_col:
    # FIX: Use key="selected_lang" so the widget is directly bound to
    # session_state.selected_lang. This means:
    # - Any rerun (file upload, GPS, etc.) keeps the selectbox on the
    #   correct language automatically — no index desync possible.
    # - We no longer need to read the return value and call st.rerun().
    lang_keys = list(lang_codes.keys())
    # Ensure the stored value is valid (safety guard)
    if st.session_state.selected_lang not in lang_keys:
        st.session_state.selected_lang = "English"

    prev_lang = st.session_state.selected_lang
    st.selectbox(
        "🌐", lang_keys,
        key="selected_lang",          # ← directly bound, no index= needed
        label_visibility="collapsed"
    )
    # If user changed it manually, record that so GPS won't overwrite later
    if st.session_state.selected_lang != prev_lang:
        st.session_state.lang_user_chosen = True
        st.rerun()

# ── Hero Header ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-wrap">
  <div style="font-size:3.2em;line-height:1.1;">🌿</div>
  <h1 style="color:#1b5e20;margin:0.10em 1.1em;font-size:2.4em;font-weight:800;
             letter-spacing:-0.5px;text-shadow:0 2px 8px rgba(27,94,32,0.10);">
    {translate("Leaf Disease Detection")}
  </h1>
  <p style="color:#558b2f;font-size:1.1em;margin:0;font-weight:500;opacity:0.9;">
    {translate("Upload a leaf image to detect diseases and get expert recommendations.")}
  </p>
</div>
""", unsafe_allow_html=True)

api_url = os.getenv("API_URL", "https://your-railway-url.up.railway.app")

# ── Two-column layout ──────────────────────────────────────────────────────────
left_col, right_col = st.columns([1, 2], gap="large")

with left_col:
    uploaded_file = st.file_uploader(
        translate("Upload Leaf Image"),
        type=["jpg", "jpeg", "png"],
        label_visibility="visible",
        key="file_uploader_main"
    )

    if uploaded_file:
        # New file uploaded — save to session state
        st.session_state.uploaded_bytes = uploaded_file.getvalue()
        st.session_state.uploaded_name  = uploaded_file.name
        st.image(uploaded_file, caption=translate("Preview"), use_container_width=True)
    elif st.session_state.uploaded_bytes is not None:
        # The built-in small X was clicked (uploaded_file is None but cached bytes exist)
        # Clear everything so results also disappear
        st.session_state.uploaded_bytes   = None
        st.session_state.uploaded_name    = None
        st.session_state.disease_result   = None
        st.session_state.result_file_name = None

# ── render_disease_result: all rendering in one place ─────────────────────────
def render_disease_result(result):
    """
    Renders the full disease result card from a result dict.
    Called after fresh API call AND on every rerun (language change, scroll).
    Reading from session state means no second API call is needed.
    """
    severity     = (result.get("severity") or "").strip().lower()
    disease_det  = result.get("disease_detected", False)
    disease_type = result.get("disease_type", "")
    confidence   = float(result.get("confidence", 0))
    plant_name   = (result.get("plant_name") or "").strip()
    if not plant_name or plant_name.lower() in ("unknown", "n/a", "none", ""):
        plant_name = "Unknown"
    theme = severity_theme(severity, disease_det)

    # ── INVALID IMAGE ──────────────────────────────────────────────────────
    if disease_type == "invalid_image":
        st.markdown(f"<div style='font-size:2em;font-weight:800;color:#f57f17;margin-bottom:0.3em;'>{translate('⚠️ Invalid Image')}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='color:#795548;font-size:1em;margin-bottom:1em;'>{translate('Please upload a clear image of a plant leaf for accurate disease detection.')}</div>", unsafe_allow_html=True)

    # ── DISEASE DETECTED ───────────────────────────────────────────────────
    elif disease_det:
        health_score = calc_health_score(confidence, severity, True)
        urg_text  = translate(urgency_key(severity, True, health_score))
        urg_style = urgency_style(severity, True, health_score)

        # Title
        st.markdown(f"<div style='font-size:2em;font-weight:800;color:{theme['title_color']};margin-bottom:0.15em;letter-spacing:-0.5px;'>🦠 {translate_grok(result.get('disease_name','N/A'))}</div>", unsafe_allow_html=True)

        # Plant name badge
        st.markdown(f"<div style='margin-bottom:0.5em;'><span class='chip' style='background:#e8f5e9;color:#1b5e20;border:1.5px solid #a5d6a720;font-size:1em;'>🌿 {translate('Plant')}: {translate_grok(plant_name)}</span></div>", unsafe_allow_html=True)

        # Urgency banner
        st.markdown(f"<div class='urgency' style='{urg_style}'>{urg_text}</div>", unsafe_allow_html=True)

        # Chips row
        st.markdown(f"""
        <div style='margin-bottom:0.5em;'>
          <span class='chip' style='background:{theme["badge_bg"]};color:{theme["accent"]};border:1.5px solid {theme["border"]}20;'>
            🧬 {translate('Type')}: {translate_grok(disease_type)}
          </span>
          <span class='chip' style='background:{theme["badge_bg"]};color:{theme["accent"]};border:1.5px solid {theme["border"]}20;'>
            📊 {translate('Severity')}: {translate_grok(severity)}
          </span>
        </div>
        """, unsafe_allow_html=True)

        # Animated confidence gauge
        st.markdown(
            confidence_gauge_html(confidence, theme["gauge_color"], translate("Confidence"),
                           disease_detected=True, severity=severity,
                           t_leaf_health=translate("Leaf Health"),
                           t_leaf_score=translate("Leaf Health Score"),
                           t_healthy=translate("Healthy"),
                           t_at_risk=translate("At Risk"),
                           t_diseased=translate("Diseased"),
                           t_zone0=translate("0–40 Diseased"),
                           t_zone1=translate("40–70 At Risk"),
                           t_zone2=translate("70–100 Healthy")),
            unsafe_allow_html=True
        )

        # Symptoms
        st.markdown(f"<div class='section-title' style='color:#e53935;'>🔴 {translate('Symptoms')}</div>", unsafe_allow_html=True)
        st.markdown("<ul class='sym-list'>", unsafe_allow_html=True)
        for s in translate_grok_list(result.get("symptoms", [])):
            st.markdown(f"<li>{s}</li>", unsafe_allow_html=True)
        st.markdown("</ul>", unsafe_allow_html=True)

        # Causes
        st.markdown(f"<div class='section-title' style='color:#fb8c00;'>🟠 {translate('Possible Causes')}</div>", unsafe_allow_html=True)
        st.markdown("<ul class='cause-list'>", unsafe_allow_html=True)
        for c in translate_grok_list(result.get("possible_causes", [])):
            st.markdown(f"<li>{c}</li>", unsafe_allow_html=True)
        st.markdown("</ul>", unsafe_allow_html=True)

        # Treatment
        st.markdown(f"<div class='section-title' style='color:#2e7d32;'>💊 {translate('Treatment')}</div>", unsafe_allow_html=True)
        st.markdown("<ul class='treat-list'>", unsafe_allow_html=True)
        for t in translate_grok_list(result.get("treatment", [])):
            st.markdown(f"<li>{t}</li>", unsafe_allow_html=True)
        st.markdown("</ul>", unsafe_allow_html=True)

        # Prevention
        prevention = result.get("prevention", [])
        if prevention:
            st.markdown(f"<div class='section-title' style='color:#1565c0;'>{translate('🛡️ Prevention')}</div>", unsafe_allow_html=True)
            st.markdown("<ul class='treat-list'>", unsafe_allow_html=True)
            for p in translate_grok_list(prevention):
                st.markdown(f"<li>{p}</li>", unsafe_allow_html=True)
            st.markdown("</ul>", unsafe_allow_html=True)

        # Affected Area + Spread Risk chips
        affected = result.get("affected_area_percent", 0)
        spread   = result.get("spread_risk", "")
        if affected or spread:
            spread_colors = {"high":"#c62828","medium":"#e65100","low":"#2e7d32","none":"#757575"}
            spread_bgs    = {"high":"#ffebee","medium":"#fff3e0","low":"#e8f5e9","none":"#f5f5f5"}
            sc = spread_colors.get((spread or "").lower(), "#757575")
            sb = spread_bgs.get((spread or "").lower(), "#f5f5f5")
            chips_html = "<div style='margin:0.7em 0;'>"
            if affected:
                chips_html += f"<span class='chip' style='background:#e3f2fd;color:#1565c0;border:1.5px solid #90caf920;'>🍂 {translate('Affected Area')}: {affected}%</span>"
            if spread:
                chips_html += f"<span class='chip' style='background:{sb};color:{sc};border:1.5px solid {sc}20;'>⚡ {translate('Spread Risk')}: {translate_grok(spread)}</span>"
            chips_html += "</div>"
            st.markdown(chips_html, unsafe_allow_html=True)

        # Expert recommendation
        extra = result.get("ai_explanation") or result.get("grok_answer") or result.get("expert_recommendation")
        if extra:
            st.markdown(f"<div class='section-title' style='color:#6a1b9a;'>🎓 {translate('Expert Recommendation')}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='background:rgba(237,231,246,0.7);border-left:4px solid #7b1fa2;border-radius:10px;padding:1em 1.2em;font-size:1em;color:#4a148c;line-height:1.75;'>{translate_grok(extra)}</div>", unsafe_allow_html=True)

        st.markdown(f"<div class='ts'>🕐 {result.get('analysis_timestamp','N/A')}</div>", unsafe_allow_html=True)

    # ── HEALTHY ────────────────────────────────────────────────────────────
    else:
        urg_text  = translate(urgency_key("", False))
        urg_style = urgency_style("", False)
        theme     = severity_theme("", False)

        st.markdown(f"<div style='font-size:2em;font-weight:800;color:{theme['title_color']};margin-bottom:0.15em;'>{translate('✅ Healthy Leaf')}</div>", unsafe_allow_html=True)

        # Plant name badge
        st.markdown(f"<div style='margin-bottom:0.5em;'><span class='chip' style='background:#e8f5e9;color:#1b5e20;border:1.5px solid #a5d6a720;font-size:1em;'>🌿 {translate('Plant')}: {translate_grok(plant_name)}</span></div>", unsafe_allow_html=True)

        st.markdown(f"<div class='urgency' style='{urg_style}'>{urg_text}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='color:#388e3c;font-size:1.05em;margin-bottom:0.8em;'>{translate('No disease detected in this leaf. The plant appears to be healthy!')}</div>", unsafe_allow_html=True)

        st.markdown(f"""<span class='chip' style='background:{theme["badge_bg"]};color:{theme["accent"]};border:1.5px solid {theme["border"]}20;'>
          ✅ {translate('Status')}: {translate_grok(disease_type or 'healthy')}
        </span>""", unsafe_allow_html=True)

        # Confidence gauge
        st.markdown(
            confidence_gauge_html(confidence, theme["gauge_color"], translate("Confidence"),
                           disease_detected=False, severity=""),
            unsafe_allow_html=True
        )

        st.markdown(f"<div class='ts'>🕐 {result.get('analysis_timestamp','N/A')}</div>", unsafe_allow_html=True)


# ── Use fresh upload OR cached bytes ──────────────────────────────────────────
active_bytes = None
active_name  = None
if uploaded_file:
    active_bytes = uploaded_file.getvalue()
    active_name  = uploaded_file.name
elif st.session_state.uploaded_bytes is not None:
    active_bytes = st.session_state.uploaded_bytes
    active_name  = st.session_state.uploaded_name

# ── Two-column layout ──────────────────────────────────────────────────────────
with right_col:
    if active_bytes:
        # ── File change detection: new file → clear cached result ──────────
        if st.session_state.result_file_name != active_name:
            st.session_state.disease_result   = None
            st.session_state.result_file_name = None

        detect_btn = st.button(
            translate("🔍 Detect Disease"),
            use_container_width=True,
            key="detect_btn"
        )

        if detect_btn:
            with st.spinner(translate("Analyzing image and contacting API...")):
                try:
                    files    = {"file": (active_name, active_bytes, "image/jpeg")}
                    response = requests.post(f"{api_url}/disease-detection-file", files=files, timeout=30)

                    if response.status_code == 200:
                        # Save result to session state so reruns (language change) can re-render it
                        st.session_state.disease_result   = response.json()
                        st.session_state.result_file_name = active_name
                        render_disease_result(st.session_state.disease_result)
                    else:
                        st.error(translate(f"API Error: {response.status_code}"))
                        st.write(response.text)

                except requests.exceptions.Timeout:
                    st.error(translate("Request timed out. The API might be processing a large image or is slow to respond."))
                except requests.exceptions.ConnectionError:
                    st.error(translate("Cannot connect to API server. Please make sure the backend is running!"))
                    st.info(translate("Run: python run_backend.py in a separate terminal"))
                except Exception as e:
                    st.error(translate(f"Error: {str(e)}"))

        # ── Re-render cached result on every rerun (language change, scroll) ──
        elif st.session_state.disease_result is not None:
            render_disease_result(st.session_state.disease_result)