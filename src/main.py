from aiortc import RTCSessionDescription, RTCPeerConnection
from aiortc.contrib.media import MediaPlayer, MediaRelay, MediaBlackhole
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import HTMLResponse

from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate, Offer
from operations.router import router as router_operation
from pages.router import router as router_pages

templates = Jinja2Templates(directory="templates")

app = FastAPI(
    title="Fitness App"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)


def create_local_tracks(play_from=None):
    if play_from:
        player = MediaPlayer(play_from)
        return player.audio, player.video
    else:
        options = {"framerate": "30", "video_size": "1920x1080", "probesize": "32M"}
        # if relay is None:
        # if platform.system() == "Darwin":
        # webcam = MediaPlayer(
        #     "default:none", format="avfoundation", options=options
        # )
        # elif platform.system() == "Windows":
        # webcam = MediaPlayer("video.mp4")
        webcam = MediaPlayer(
            "default:none", format="avfoundation", options=options
        )

        # else:
        # webcam = MediaPlayer("/dev/video0", format="v4l2", options=options)
        # audio, video = VideoTransformTrack(webcam.video, transform="cv")
        relay = MediaRelay()
        return None, relay.subscribe(webcam.video)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


app.include_router(router_operation)
app.include_router(router_pages)


@app.post("/offer")
async def offer(params: Offer):
    offer = RTCSessionDescription(sdp=params.sdp, type=params.type)

    pc = RTCPeerConnection()
    pcs.add(pc)
    recorder = MediaBlackhole()

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        print("Connection state is %s" % pc.connectionState)
        if pc.connectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    # open media source
    audio, video = create_local_tracks()

    # handle offer
    await pc.setRemoteDescription(offer)
    await recorder.start()

    # send answer
    answer = await pc.createAnswer()

    await pc.setRemoteDescription(offer)
    for t in pc.getTransceivers():
        if t.kind == "audio" and audio:
            pc.addTrack(audio)
        elif t.kind == "video" and video:
            pc.addTrack(video)

    await pc.setLocalDescription(answer)

    return {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}


pcs = set()
