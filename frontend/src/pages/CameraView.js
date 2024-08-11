import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import {
  faEye,
  faAngleLeft,
  faAngleRight,
} from "@fortawesome/free-solid-svg-icons";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

const CameraView = () => {
  const { id } = useParams();
  const [camera, setCamera] = useState(null);
  const [recordingInfo, setRecordingInfo] = useState(null);
  const [recordingTimeline, setRecordingTimeline] = useState(null);
  const navigate = useNavigate();
  const accessToken = localStorage.getItem("accessToken");

  useEffect(() => {
    if (!accessToken) {
      navigate("/login");
    }
    console.log(accessToken);
  }, [navigate]);

  useEffect(() => {
    const controller = new AbortController();
    const signal = controller.signal;
    const fetchCamera = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/camera/${id}`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        setCamera(data);
      } catch (error) {
        console.error("Error fetching cameras:", error);
      }
    };

    const fetchCameraRecordingRecordingInfo = async () => {
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/api/camera/${id}/recording/info`,
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
        setRecordingInfo(data);
      } catch (error) {
        console.error("Error fetching recording info:", error);
      }
    };

    fetchCamera();
    fetchCameraRecordingRecordingInfo();
    return () => {
      controller.abort();
    };
  }, [id]);

  useEffect(() => {
    const fetchCameraRecordingTimelnes = async (start, end) => {
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/api/camera/${id}/recording/timeline/?start=${start}&end=${end}`,
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
        setRecordingTimeline(data.segments);
      } catch (error) {
        console.error("Error fetching timeline:", error);
      }
    };
    // Parse the recording_start timestamp
    const recordingStartDate = new Date(
      recordingInfo ? recordingInfo.recording_end : ""
    );

    if (recordingInfo) {
      const previous24HoursDate = new Date(
        recordingStartDate.getTime() - 23 * 60 * 60 * 1000
      );

      // Format the new timestamp as an ISO 8601 string
      const formattedPrevious24Hours = previous24HoursDate.toISOString();

      fetchCameraRecordingTimelnes(
        formattedPrevious24Hours,
        recordingInfo.recording_end
      );
    }
  }, [recordingInfo]);

  const handleSegmentClick = (start, end) => {
    navigate(
      `/segment/${id}?start=${encodeURIComponent(
        start
      )}&end=${encodeURIComponent(end)}`
    );
  };

  const dataForButtons = [
    {
      name: <FontAwesomeIcon icon={faEye} />,
      className: "",
      onClick: () => alert("Icon1 clicked"),
    },
    {
      name: <FontAwesomeIcon icon={faAngleLeft} />,
      className: "",
      onClick: () => alert("Icon2 clicked"),
    },
    {
      name: <FontAwesomeIcon icon={faAngleRight} />,
      className: "",
      onClick: () => alert("Icon3 clicked"),
    },
  ];

  return (
    <div className="flex flex-col min-h-screen justify-between">
      <Navbar />
      <div className="flex justify-center items-center">
        {!camera ? (
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
        ) : (
          <>
            <main className="flex-grow container mx-auto p-4 flex items-center flex-col">
              <div className="w-full justfy-start mt-7">
                <h2 className="text-xl font-semibold">
                  Camera Owner Information
                </h2>
                <ul className="list-disc pl-5 space-y-1 mt-5">
                  <li className="flex flex-row space-x-2">
                    <strong>
                      <p>Email: </p>
                    </strong>
                    <span>{camera.owner.email}</span>
                  </li>
                  <li className="flex flex-row space-x-2">
                    <strong>
                      <p>Name: </p>
                    </strong>
                    {camera.owner.first_name} {camera.owner.last_name}
                  </li>
                </ul>
              </div>
              <h1 className="text-2xl font-bold mb-8">{camera.name}</h1>
              <div className="bg-card-bg text-white p-4 rounded-lg max-w-[1000px]  w-[1000px]">
                <div className="mt-4">
                  {camera.streams.length > 1 ? (
                    // Check if there's more than one stream
                    camera.streams[1].format === "mp4" ? (
                      <video
                        src={camera.streams[1].url}
                        autoPlay
                        muted
                        className="w-[1000px] h-[500px] rounded-lg"
                        onError={(e) =>
                          console.error("Video failed to load:", e)
                        }
                      >
                        Your browser does not support the video tag.
                      </video>
                    ) : (
                      <p>Unsupported stream format</p>
                    )
                  ) : camera.streams.length > 0 &&
                    camera.streams.length <= 1 ? (
                    // Check if there's exactly one stream
                    camera.streams[0].format === "mjpeg" ? (
                      <img
                        src={camera.streams[0].url}
                        alt="MJPEG stream"
                        className="w-[1000px] h-[500px] rounded-lg"
                      />
                    ) : (
                      <p>Unsupported stream format</p>
                    )
                  ) : (
                    // No streams available
                    <p>No streams available</p>
                  )}
                </div>

                {camera.streams.length > 0 && (
                  <div className="mt-4">
                    <a
                      href={camera.streams[0].url}
                      className="text-white hover:text-blue-500"
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      View Live Stream in New Tab
                    </a>
                  </div>
                )}
              </div>

              {recordingInfo ? (
                <div className=" hadow-xl w-full flex justify-between p-3 rounded mt-5">
                  <div className="w-auto p-3 rounded-lg shadow-lg bg-card-bg text-white">
                    <div className="font-semibold">Recording Status</div>
                    <span class="bg-green-100 text-green-800 text-xs font-medium me-2 px-2.5 py-0.5 rounded dark:bg-green-900 dark:text-green-300">
                      {recordingInfo ? recordingInfo.status : null}
                    </span>

                    <div></div>
                  </div>
                  <div className="w-auto p-3 rounded-lg shadow-lg bg-card-bg text-white">
                    <div className="font-semibold">Recording Retention</div>
                    <div>{recordingInfo ? recordingInfo.retention : null}</div>
                  </div>
                  <div className="w-auto p-3 rounded-lg shadow-lg bg-card-bg text-white">
                    <div className="font-semibold">Recording Start</div>
                    <div>
                      {recordingInfo
                        ? new Date(
                            recordingInfo.recording_start
                          ).toLocaleString()
                        : null}
                    </div>
                  </div>
                  <div className="w-auto p-3 rounded-lg shadow-lg bg-card-bg text-white">
                    <div className="font-semibold">Recording End</div>
                    <div>
                      {recordingInfo
                        ? new Date(recordingInfo.recording_end).toLocaleString()
                        : null}
                    </div>
                  </div>
                </div>
              ) : null}
              {recordingTimeline ? (
                <div className="mt-8 w-full mb-7">
                  <h2 className="text-xl font-semibold mb-4">
                    Recording Segments
                  </h2>
                  <div className="overflow-x-auto">
                    <div className="flex space-x-4 ">
                      <p></p>
                      {recordingTimeline?.map((segment, index) => (
                        <div
                          key={index}
                          className="flex-shrink-0 bg-segment-bg border border-gray-300 rounded-lg p-4 shadow-lg cursor-pointer transform transition-transform duration-500 hover:scale-105"
                          style={{ minWidth: "200px" }}
                          onClick={() =>
                            handleSegmentClick(segment.start, segment.end)
                          }
                        >
                          <h3 className="text-lg font-semibold mb-2">
                            Segment {index + 1}
                          </h3>
                          <p className="text-gray-700">
                            <strong>Start:</strong>{" "}
                            {new Date(segment.start).toLocaleString()}
                          </p>
                          <p className="text-gray-700">
                            <strong>End:</strong>{" "}
                            {new Date(segment.end).toLocaleString()}
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              ) : null}
            </main>
          </>
        )}
      </div>
      <Footer />
    </div>
  );
};

export default CameraView;
