# Calisthenics Coach

Real-time AI-powered form coach for bodyweight exercises. Uses computer vision to watch your movements and gives instant voice feedback on technique, counts reps, and scores your form.

## What it does

Point your camera at yourself doing push-ups, squats, or pull-ups. The AI coach watches your form in real-time using YOLO pose detection, counts your reps automatically, and tells you what you're doing right (or wrong). It's like having a personal trainer who never gets tired of watching you exercise.

## Exercises supported

- Push-ups
- Squats  
- Pull-ups
- Planks
- Dips
- Burpees

Each exercise has detailed coaching instructions that tell the AI exactly what good form looks like.

## How it works

The system uses three main pieces:

1. **YOLO pose detection** - Computer vision model that identifies 17 keypoints on your body (shoulders, elbows, hips, knees, etc.)
2. **Gemini Realtime** - Google's multimodal AI that analyzes your movements and speaks coaching feedback
3. **Stream Video** - Infrastructure for real-time video processing

When you do a push-up, YOLO tracks your elbow angle. The AI knows that proper form means elbows should reach 90 degrees at the bottom. If you're not going deep enough, it tells you. If your hips are sagging, it catches that too.

## Tech stack

- Python 3.10+
- Vision Agents SDK (handles the YOLO + AI integration)
- Gemini API (voice feedback)
- Stream Video API (video infrastructure)
- Ultralytics YOLO (pose detection model)

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/calisthenics-coach.git
cd calisthenics-coach
```

### 2. Install dependencies

Using uv (recommended):
```bash
uv sync
```

Or with pip:
```bash
pip install -r requirements.txt
```

### 3. Get API keys

You need three API keys:

**Google AI Studio** (for Gemini):
- Go to https://aistudio.google.com/apikey
- Create a new API key
- Copy it

**Stream** (for video):
- Sign up at https://getstream.io/
- Create an app
- Get your API key and secret from dashboard

### 4. Configure environment

Create a `.env` file:

```bash
GOOGLE_API_KEY=your_google_api_key_here
STREAM_API_KEY=your_stream_api_key_here
STREAM_API_SECRET=your_stream_api_secret_here
```

### 5. Run it

```bash
python backend_simple.py run
```

A browser window opens with a video call interface. Grant camera permission. The coach introduces itself. Start doing push-ups and it'll count your reps and give you feedback.

## Project structure

```
calisthenics-coach/
├── backend_simple.py           # Main entry point
├── instructions/
│   ├── pushups.md             # Push-up coaching guide
│   ├── squats.md              # Squat coaching guide
│   ├── pullups.md             # Pull-up coaching guide
│   ├── planks.md              # Plank coaching guide
│   ├── dips.md                # Dip coaching guide
│   └── burpees.md             # Burpee coaching guide
├── .env                       # API keys (create this)
├── README.md                  # You are here
└── pyproject.toml            # Project metadata
```

## Customizing exercises

Want to change what the coach looks for? Edit the instruction files in `instructions/`. Each file tells the AI what good form looks like for that exercise.

For example, `instructions/pushups.md` includes criteria like:
- Elbow angle should reach 90° at bottom
- Body should stay straight (no hip sag)
- Head stays neutral
- Full range of motion

The AI reads these instructions and watches for violations.

## Changing exercises

Open `backend_simple.py` and change this line:

```python
SELECTED_EXERCISE = "pushups"  # Change to: squats, pullups, planks, dips, burpees
```

## Performance notes

YOLO runs on CPU by default. This works fine but processes ~10-15 FPS. If you have an NVIDIA GPU, change this in `backend_simple.py`:

```python
device="cpu"  # Change to "cuda"
```

With GPU you'll get 30+ FPS which makes tracking smoother.

## How rep counting works

The AI doesn't count reps by detecting motion. It measures angles.

For push-ups:
- Measures the angle between your shoulder, elbow, and wrist
- When angle goes below 100° → you're in the down position
- When angle goes above 150° → you're in the up position  
- Down → Up transition = one rep counted

For squats:
- Compares hip position to knee position
- When hips drop below knees → down position
- When hips rise above knees → up position
- Down → Up transition = one rep

This is more reliable than just tracking movement because it ensures you're actually doing the full range of motion.

## Scoring system

Each rep gets scored 1-10 based on form quality.

The AI checks:
- Did you go through full range of motion?
- Was your body aligned correctly?
- Did you maintain proper posture?

A perfect rep (score 10) means you nailed all the form criteria. A score of 5-6 means you completed the rep but with form issues. Below 5 means significant problems.

## Limitations

- Needs good lighting for YOLO to detect your body
- Camera should see your full body (not just upper body)
- Works best if you're the only person in frame
- CPU processing means ~10 FPS (fine for coaching, not high-speed analysis)

## Built for Vision Agents hackathon

This project was built for the Vision Possible: Agent Protocol hackathon (Feb 23 - Mar 1, 2026). The challenge was to build something using Vision Agents SDK that combines computer vision with AI agents.

We picked calisthenics coaching because:
1. Form really matters for bodyweight exercises
2. It's hard to see your own form mistakes
3. Real-time feedback is crucial
4. Perfect use case for pose detection + AI feedback

## License

MIT - do whatever you want with it

## Contributing

Have ideas for better rep detection? Different exercises? Better scoring? Open an issue or PR.

## Acknowledgments

- Vision Agents SDK team for making this easier than it should be
- Ultralytics for YOLO
- Google for Gemini
- Stream for video infrastructure