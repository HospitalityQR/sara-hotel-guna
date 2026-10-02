/**
 * ============================================================================
 *  HOTEL THE SARA (गुना, मध्य प्रदेश) — CENTRAL BRAND & SECURITY CONFIGURATION
 * ============================================================================
 *  Stay in Style • Multi-Cuisine Luxury Dining, Banquets & Executive Stays
 *  AB Road, Near Kushmoda Chowki, Gaushala Mahaveerpura, Guna (M.P.)
 * ============================================================================
 */

window.RESTAURANT_CONFIG = {
    // 1. Brand Identity
    name: "Hotel The Sara",
    subname: "HOTEL THE SARA",
    tagline: "STAY IN STYLE • LUXURY DINING & BANQUETS",
    cityTagline: "AB ROAD • GUNA (M.P.)",
    highlight: "Multi-Cuisine Fine Dining • Royal Celebrations • Executive Rooms",
    diningHighlight: "Hygienic Family Dining • Grand Banquets • Premium Hospitality",

    // Primary Address & Location Details
    addressPrimaryLabel: "LOCATION",
    addressPrimary: "AB Road, Near Kushmoda Chowki, Gaushala Mahaveerpura, Guna, Madhya Pradesh 473001",
    city: "Guna, Madhya Pradesh",

    // Contact Numbers
    phone: "9303284300",
    phoneDisplay: "+91 93032 84300",
    altPhone: "7542268068",
    altPhoneDisplay: "+91 75422 68068",
    whatsapp: "9303284300",
    whatsappDisplay: "+91 93032 84300",
    whatsappUrl: "https://wa.me/919303284300?text=Namaste%20Hotel%20The%20Sara%2C%20I%20would%20like%20to%20connect%20for%20dining%20%2F%20room%20reservation.",

    // Brand Assets
    logoUrl: "logo_medallion.png",
    logoCleanUrl: "sara_logo_clean.png",
    bgUrl: "bg_ambience_brownish.jpg",

    // Ambience Showcase Photos
    ambiencePhotos: [
        "ambience_1.jpg?v=1",
        "ambience_2.jpg?v=1",
        "ambience_3.jpg?v=1"
    ],

    // 2. Exact Action Destination Links
    googleReviewUrl: "https://share.google/vRFMikseO8TDcpg9l",
    instagramUrl: "https://www.instagram.com/hotelthesara?stkn=dzQwc3pzNGx0Y3Jo",
    instagramHandle: "@hotelthesara",
    landingPageUrl: "https://hospitalityqr.github.io/sara-hotel-guna/",

    // 3. Auto-Redirect Behavior (Optional)
    autoRedirectToGoogle: false,
    autoRedirectDelayMs: 1200,

    // ========================================================================
    // 4. LIVE WHATSAPP MANAGER ALERT (SMART REVIEW FILTER)
    // ========================================================================
    // ⭐ 4 or 5 Stars -> Direct to Google Review!
    // ⚠️ 1, 2, or 3 Stars -> BLOCKS Google & Sends Instant Alert to Manager's WhatsApp!
    managerAlert: {
        enabled: true,
        // होटल मालिक या मैनेजर का WhatsApp नंबर जिस पर अलर्ट जाएगा:
        managerWhatsApp: "9303284300",
        
        // कितने स्टार पर Google रिव्यू भेजना है (4 और 5 स्टार = Good)
        // 1, 2, 3 स्टार पर WhatsApp अलर्ट जाएगा:
        minGoodStars: 4,

        // होटल का नाम जो मैसेज में जाएगा:
        hotelName: "Hotel The Sara, Guna",

        // मैसेज की हेडिंग:
        alertHeading: "🚨 URGENT GUEST COMPLAINT ALERT",

        // क्विक इश्यू ऑप्शंस जो कस्टमर सिलेक्ट कर सकता है:
        issueCategories: [
            "🍲 Food Taste / Quality Issue",
            "⏱️ Slow Service / Waiter Delay",
            "❄️ AC / Ambience / Noise",
            "🧼 Cleanliness / Hygiene Issue",
            "🧾 Billing / Pricing Query"
        ]
    },

    // ========================================================================
    // 5. ANTI-COPY & DIGITAL LICENSE PROTECTION ENGINE (ANTI-THEFT LOCK)
    // ========================================================================
    license: {
        enabled: true,
        status: "ACTIVE", // Options: "ACTIVE", "LOCKED", "TRIAL"
        authorizedStandeesCount: 1,
        serialNumber: "HS-GUNA-VIP-001",
        tableNumber: "VIP TABLE #01",
        enableDailyScanLimit: true,
        maxDailyScans: 60,
        lockTitle: "AUTHENTIC HARDWARE LICENSE VERIFICATION",
        lockMessage: "This Smart Hospitality Hub is registered for Single Table Display (#HS-GUNA-001). Multiple simultaneous scans detected. To activate multi-table dining service, contact your authorized provider.",
        vendorContact: "+91-XXXXXXXXXX (Authorized Provider)"
    }
};
