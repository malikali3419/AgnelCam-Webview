import React, { useEffect, useState, useRef } from "react";
import { useLocation, useParams } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import Hls from "hls.js";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

const VideoSegmentView = () => {
  const location = useLocation();
  const query = new URLSearchParams(location.search);
  const navigate = useNavigate();
  const start = query.get("start");
  const end = query.get("end");
  const [hlsUrl, setHlsUrl] = useState(null);
  const { id } = useParams();
  const videoRef = useRef(null);
  const accessToken = localStorage.getItem("accessToken");

  useEffect(() => {
    if (!accessToken) {
      navigate("/login");
    }
  }, [navigate]);
  useEffect(() => {
    const fetchVideoUrl = async () => {
      if (start && end) {
        try {
          const response = await fetch(
            `http://127.0.0.1:8000/api/camera/${id}/recording/stream?start=${start}&end=${end}`,
            {
              method: "GET",
              headers: {
                Authorization: `Bearer ${accessToken}`,
              },
            }
          );

          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }

          const data = await response.json();
          setHlsUrl(data.url); // Use the URL fetched from API
        } catch (error) {
          console.error("Error fetching video URL:", error);
        }
      }
    };

    fetchVideoUrl();
  }, [start, end, id]);

  // Initialize HLS.js if supported or use native HLS playback
  useEffect(() => {
    if (hlsUrl) {
      const videoElement = videoRef.current;

      if (Hls.isSupported()) {
        const hls = new Hls({ debug: true });

        hls.loadSource(hlsUrl);
        hls.attachMedia(videoElement);

        hls.on(Hls.Events.MANIFEST_PARSED, () => {
          videoElement.play().catch((error) => {
            console.error("Playback error:", error);
          });
        });

        hls.on(Hls.Events.ERROR, (event, data) => {
          console.error("HLS.js error:", event, data);
          if (data.details === "manifestLoadError") {
            console.error("Error loading manifest:", data.response);
          } else if (
            data.details === "levelLoadError" ||
            data.details === "fragLoadError"
          ) {
            console.error("Error loading segment:", data.response);
          }
        });

        hls.on(Hls.Events.BUFFER_FLUSHING, () => {
          console.log("Buffer flushing...");
        });

        hls.on(Hls.Events.LEVEL_LOADED, () => {
          console.log("Levels loaded.");
        });

        hls.on(Hls.Events.FRAG_LOADED, () => {
          console.log("Fragment loaded.");
        });

        return () => {
          hls.destroy();
        };
      } else if (videoElement.canPlayType("application/vnd.apple.mpegurl")) {
        videoElement.src = hlsUrl;
        videoElement.addEventListener("loadedmetadata", () => {
          videoElement.play().catch((error) => {
            console.error("Playback error:", error);
          });
        });
      } else {
        console.error("HLS is not supported");
      }
    }
  }, [hlsUrl]);

  return (
    <div className="flex flex-col justify-between">
      <Navbar />
      <div className="flex items-center justify-center h-[100vh] p-5">
        {hlsUrl ? (
          <div className="bg-card-bg text-white p-4 rounded-lg max-w-full w-full">
            <div className=" inset-0">
              {hlsUrl ? (
                <video
                  ref={videoRef}
                  controls
                  autoPlay
                  muted
                  style={{
                    width: "100%",
                    objectFit: "cover",
                    backgroundColor: "#000",
                  }}
                >
                  Your browser does not support the video tag.
                </video>
              ) : (
                <div>Loading...</div>
              )}
            </div>
          </div>
        ) : (
          <div role="status">
            <svg
              aria-hidden="true"
              class="w-32 h-32 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
              viewBox="0 0 100 101"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                fill="currentColor"
              />
              <path
                d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                fill="currentFill"
              />
            </svg>
            <span class="sr-only">Loading...</span>
          </div>
        )}
      </div>
      <Footer />
    </div>
  );
};

export default VideoSegmentView;
