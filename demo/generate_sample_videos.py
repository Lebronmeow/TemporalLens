"""
Generates high-fidelity demonstration benchmark videos for TemporalLens AI workstation.
Creates:
  - demo/samples/sample_cooking.mp4
  - demo/samples/sample_sports.mp4
  - demo/samples/sample_daily_routine.mp4
"""

import os
from pathlib import Path
import cv2
import numpy as np

def create_video(
    output_path: str,
    duration_sec: float = 10.0,
    fps: float = 24.0,
    title: str = "Demo Sequence",
    action_span: tuple[float, float] = (3.5, 7.5),
    action_label: str = "Target Action",
    base_image_path: str | None = None,
    color_theme: tuple[int, int, int] = (30, 30, 35) # BGR
):
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    width, height = 1280, 720
    total_frames = int(duration_sec * fps)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    base_img = None
    if base_image_path and os.path.exists(base_image_path):
        loaded = cv2.imread(base_image_path)
        if loaded is not None:
            base_img = cv2.resize(loaded, (width, height))

    s_action, e_action = action_span

    for i in range(total_frames):
        t = i / fps
        is_action = s_action <= t <= e_action

        # Base frame background
        if base_img is not None:
            # Subtle slow zoom/pan effect for natural motion
            zoom_factor = 1.0 + 0.08 * (i / total_frames)
            center_x, center_y = width // 2, height // 2
            M = cv2.getRotationMatrix2D((center_x, center_y), 0, zoom_factor)
            frame = cv2.warpAffine(base_img, M, (width, height), flags=cv2.INTER_LINEAR)
        else:
            frame = np.full((height, width, 3), color_theme, dtype=np.uint8)

        # Apply dark cinematic vignette & styling
        overlay = frame.copy()
        
        # Bottom HUD bar
        cv2.rectangle(overlay, (0, height - 70), (width, height), (9, 9, 11), -1)
        cv2.line(overlay, (0, height - 70), (width, height - 70), (39, 39, 42), 1)

        # Top HUD bar
        cv2.rectangle(overlay, (0, 0), (width, 55), (9, 9, 11), -1)
        cv2.line(overlay, (0, 55), (width, 55), (39, 39, 42), 1)

        # Status indicator
        if is_action:
            # Highlight border
            cv2.rectangle(overlay, (12, 12), (width - 12, height - 12), (11, 158, 245), 2) # Cadmium Amber in BGR
            # Amber action badge
            cv2.rectangle(overlay, (24, 75), (520, 115), (20, 20, 25), -1)
            cv2.rectangle(overlay, (24, 75), (520, 115), (11, 158, 245), 1)
            cv2.putText(
                overlay,
                f"GROUNDED INTERVAL: {action_label.upper()}",
                (36, 102),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (11, 158, 245),
                1,
                cv2.LINE_AA,
            )
        else:
            cv2.rectangle(overlay, (24, 75), (380, 115), (20, 20, 25), -1)
            cv2.rectangle(overlay, (24, 75), (380, 115), (60, 60, 65), 1)
            cv2.putText(
                overlay,
                "SEARCHING VIDEO STREAM...",
                (36, 102),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (160, 160, 165),
                1,
                cv2.LINE_AA,
            )

        # Blend overlay
        frame = cv2.addWeighted(overlay, 0.95, frame, 0.05, 0)

        # SMPTE timecode (MM:SS.ff)
        m = int(t // 60)
        s = int(t % 60)
        ff = int((t - int(t)) * 100)
        smpte_str = f"SMPTE {m:02d}:{s:02d}.{ff:02d}"

        cv2.putText(
            frame,
            f"TEMPORALLENS AI // {title.upper()}",
            (24, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (245, 245, 250),
            1,
            cv2.LINE_AA,
        )

        cv2.putText(
            frame,
            f"FRAME {i+1:04d}/{total_frames:04d} ({fps:.1f} FPS)",
            (width - 320, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (160, 160, 170),
            1,
            cv2.LINE_AA,
        )

        # Bottom info
        cv2.putText(
            frame,
            smpte_str,
            (24, height - 28),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (11, 158, 245) if is_action else (220, 220, 225),
            2,
            cv2.LINE_AA,
        )

        # Progress bar
        bar_x = 320
        bar_w = width - 360
        bar_y = height - 36
        bar_h = 10
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h), (30, 30, 35), -1)
        
        # Action highlight in progress bar
        act_s_x = bar_x + int((s_action / duration_sec) * bar_w)
        act_e_x = bar_x + int((e_action / duration_sec) * bar_w)
        cv2.rectangle(frame, (act_s_x, bar_y), (act_e_x, bar_y + bar_h), (11, 158, 245), -1)

        # Current playhead
        play_x = bar_x + int((t / duration_sec) * bar_w)
        cv2.line(frame, (play_x, bar_y - 4), (play_x, bar_y + bar_h + 4), (255, 255, 255), 2)

        out.write(frame)

    out.release()
    print(f"Generated: {output_path} ({duration_sec}s, {total_frames} frames)")


def main():
    root = Path(__file__).resolve().parent
    samples_dir = root / "samples"
    samples_dir.mkdir(parents=True, exist_ok=True)
    media_dir = root.parent / "media"

    print("Generating TemporalLens demo sequence clips...")

    # 1. Culinary Action
    create_video(
        output_path=str(samples_dir / "sample_cooking.mp4"),
        duration_sec=10.0,
        fps=24.0,
        title="Culinary Action Sequence (Charades-STA)",
        action_span=(3.5, 7.5),
        action_label="Pouring oil and sauteing in pan",
        base_image_path=str(media_dir / "teaser.jpg"),
        color_theme=(25, 22, 28)
    )

    # 2. Athletic Event
    create_video(
        output_path=str(samples_dir / "sample_sports.mp4"),
        duration_sec=10.0,
        fps=24.0,
        title="Athletic Event Tracking (ActivityNet)",
        action_span=(3.0, 6.5),
        action_label="Shooting basketball towards hoop",
        base_image_path=str(media_dir / "hero-frame-3.jpg"),
        color_theme=(22, 28, 25)
    )

    # 3. Ambient Routine
    create_video(
        output_path=str(samples_dir / "sample_daily_routine.mp4"),
        duration_sec=12.0,
        fps=24.0,
        title="Ambient Routine Grounding (Ego4D-NLQ)",
        action_span=(4.0, 9.0),
        action_label="Person opens refrigerator and picks water",
        base_image_path=str(media_dir / "hero-frame-1.jpg"),
        color_theme=(28, 25, 22)
    )

    print("All sample videos generated successfully.")

if __name__ == "__main__":
    main()
