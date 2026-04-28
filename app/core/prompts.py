"""
prompts.py — BridalVision AI
==============================
Dedicated Prompt Engineering module for the virtual bridal dress try-on system.

This file contains all prompts used when calling fal.ai IDM-VTON.
Prompts are carefully crafted to produce:
  - Realistic dress fitting on real body shapes
  - Natural bridal lighting and shadow
  - High-quality photorealistic output
  - Proper background and scene placement

WHY PROMPT ENGINEERING MATTERS HERE:
  IDM-VTON is a diffusion-based model. The quality of the output
  heavily depends on how we guide the model with text prompts.
  A poorly written prompt produces unrealistic, distorted results.
  A well-crafted bridal prompt produces magazine-quality previews.

Author  : Shahidul Islam, Jr. AI Engineer
Company : Betopia Group / Join Venture AI, Dhaka, Bangladesh
"""


# ═══════════════════════════════════════════════════════════════════
# SECTION 1 — CORE BRIDAL TRY-ON PROMPTS
# ═══════════════════════════════════════════════════════════════════

# ── Main Positive Prompt ─────────────────────────────────────────
# Used for every try-on request as the base prompt.
BRIDAL_BASE_PROMPT = (
    "A beautiful bride wearing the selected wedding dress. "
    "Realistic body fitting with natural pose adaptation. "
    "Soft elegant bridal lighting, natural shadow rendering, "
    "smooth fabric texture, full-body view, high resolution, "
    "photorealistic, bridal boutique photography style, "
    "clean white or soft neutral background."
)

# ── Main Negative Prompt ─────────────────────────────────────────
# Tells the model what to AVOID generating.
BRIDAL_BASE_NEGATIVE_PROMPT = (
    "blurry, distorted body, unrealistic proportions, "
    "cartoon, painting, illustration, sketch, "
    "bad anatomy, deformed hands, extra limbs, "
    "wrong dress color, color bleeding, "
    "artifacts, watermark, logo, text, "
    "low quality, pixelated, grainy, overexposed, "
    "dark background, dirty background."
)


# ═══════════════════════════════════════════════════════════════════
# SECTION 2 — DRESS STYLE SPECIFIC PROMPTS
# Used when the dress category is known — improves output quality
# ═══════════════════════════════════════════════════════════════════

DRESS_STYLE_PROMPTS = {

    "ball_gown": (
        "Full princess ball gown wedding dress, voluminous skirt, "
        "structured bodice, dramatic silhouette, "
        "elegant bridal lighting, cathedral setting atmosphere."
    ),

    "a_line": (
        "Classic A-line wedding dress, fitted bodice flaring gently to floor, "
        "timeless bridal style, soft natural lighting, "
        "flattering silhouette on all body types."
    ),

    "mermaid": (
        "Fitted mermaid wedding dress, hugging body from chest to knee, "
        "flaring dramatically at hem, sleek and glamorous bridal style, "
        "form-fitting realistic fabric draping."
    ),

    "sheath": (
        "Slim sheath wedding dress, sleek column silhouette, "
        "minimalist modern bridal style, close to body, "
        "elegant and sophisticated, clean lines."
    ),

    "lace": (
        "Intricate lace wedding dress, delicate floral lace patterns, "
        "romantic and vintage bridal style, "
        "soft diffused lighting to highlight lace texture, "
        "feminine and timeless."
    ),

    "off_shoulder": (
        "Off-shoulder wedding dress, elegant neckline, "
        "fabric draped gracefully over shoulders, "
        "romantic bridal portrait style, "
        "natural skin tones with dress contrast."
    ),

    "default": BRIDAL_BASE_PROMPT  # Fallback if style unknown
}


# ═══════════════════════════════════════════════════════════════════
# SECTION 3 — LIGHTING SCENE PROMPTS
# Adjust based on the desired output mood
# ═══════════════════════════════════════════════════════════════════

LIGHTING_PROMPTS = {

    "studio": (
        "Professional studio lighting, soft white background, "
        "evenly lit, boutique photography, clean and bright."
    ),

    "outdoor": (
        "Golden hour outdoor lighting, garden wedding atmosphere, "
        "warm soft sunlight, natural greenery background, "
        "romantic and dreamy."
    ),

    "church": (
        "Soft cathedral lighting, warm ambient glow, "
        "elegant church interior atmosphere, "
        "dramatic yet romantic bridal lighting."
    ),

    "default": (
        "Soft natural bridal lighting, clean neutral background, "
        "professional bridal boutique photography style."
    )
}


# ═══════════════════════════════════════════════════════════════════
# SECTION 4 — BODY ADAPTATION GUIDANCE
# Extra prompt additions for better body shape fitting
# ═══════════════════════════════════════════════════════════════════

BODY_ADAPTATION_PROMPT = (
    "Dress perfectly fitted to the person's natural body shape and pose. "
    "Fabric follows body contours naturally. "
    "No warping, stretching, or unrealistic fitting. "
    "Dress adapts to the person — not the other way around."
)

POSE_PRESERVATION_PROMPT = (
    "Preserve the original pose of the person exactly. "
    "No changes to body position, hand placement, or stance. "
    "Only the clothing changes — body and face remain identical."
)


# ═══════════════════════════════════════════════════════════════════
# SECTION 5 — QUALITY BOOSTER PROMPTS
# Added to all prompts to push output quality higher
# ═══════════════════════════════════════════════════════════════════

QUALITY_BOOSTER = (
    "8K resolution, ultra detailed, sharp focus, "
    "professional fashion photography, "
    "magazine quality, award winning bridal photo."
)

QUALITY_NEGATIVE = (
    "jpeg artifacts, compression, noise, grain, "
    "overprocessed, plastic skin, doll-like appearance."
)


# ═══════════════════════════════════════════════════════════════════
# SECTION 6 — PROMPT BUILDER FUNCTION
# Call this to get the final combined prompt for any try-on request
# ═══════════════════════════════════════════════════════════════════

def build_tryon_prompt(
    dress_style : str = "default",
    lighting    : str = "default",
    boost_quality: bool = True
) -> dict:
    """
    Build the final positive and negative prompts for a try-on request.

    Combines:
      - Base bridal prompt
      - Dress style specific prompt
      - Lighting scene prompt
      - Body adaptation guidance
      - Pose preservation
      - Optional quality booster

    Args:
        dress_style   (str) : Dress category key from DRESS_STYLE_PROMPTS.
                              Options: "ball_gown", "a_line", "mermaid",
                              "sheath", "lace", "off_shoulder", "default"
        lighting      (str) : Lighting scene key from LIGHTING_PROMPTS.
                              Options: "studio", "outdoor", "church", "default"
        boost_quality (bool): Add quality booster prompt (default: True)

    Returns:
        dict: {
            "positive": str,  — Full positive prompt to send to fal.ai
            "negative": str   — Full negative prompt to send to fal.ai
        }

    Example:
        prompts = build_tryon_prompt(dress_style="lace", lighting="outdoor")
        fal_client.run(model, arguments={
            "prompt"         : prompts["positive"],
            "negative_prompt": prompts["negative"],
            ...
        })
    """

    # ── Get style-specific prompt (fallback to default) ───────────
    style_prompt   = DRESS_STYLE_PROMPTS.get(dress_style, DRESS_STYLE_PROMPTS["default"])
    lighting_prompt = LIGHTING_PROMPTS.get(lighting, LIGHTING_PROMPTS["default"])

    # ── Build positive prompt ─────────────────────────────────────
    positive_parts = [
        BRIDAL_BASE_PROMPT,
        style_prompt,
        lighting_prompt,
        BODY_ADAPTATION_PROMPT,
        POSE_PRESERVATION_PROMPT,
    ]

    if boost_quality:
        positive_parts.append(QUALITY_BOOSTER)

    positive_prompt = " ".join(positive_parts)

    # ── Build negative prompt ─────────────────────────────────────
    negative_parts = [BRIDAL_BASE_NEGATIVE_PROMPT]

    if boost_quality:
        negative_parts.append(QUALITY_NEGATIVE)

    negative_prompt = " ".join(negative_parts)

    return {
        "positive": positive_prompt,
        "negative": negative_prompt
    }


# ═══════════════════════════════════════════════════════════════════
# SECTION 7 — QUICK ACCESS (default prompts for simple use)
# ═══════════════════════════════════════════════════════════════════

# These are ready-to-use defaults — just import and use directly
DEFAULT_POSITIVE_PROMPT = build_tryon_prompt()["positive"]
DEFAULT_NEGATIVE_PROMPT = build_tryon_prompt()["negative"]