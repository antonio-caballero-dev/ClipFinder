import React from "react";


const VideoPlayer = ({ video, className }) => {
  return (
    <div className="video-player">
      <h2 className="video-player-title">ClipFinder</h2>
      {video ? (
        <video
          src={"http://localhost:8000/video/" + encodeURIComponent(video)}
          controls
          className={className || "video-player-element"}
          poster={"/video_data/" + video.replace(/\.[^/.]+$/, ".jpg")}
        >
          Tu navegador no soporta la reproducción de video.
        </video>
      ) : (
        <div className="video-player-placeholder">
          Selecciona un video de la lista para comenzar
        </div>
      )}
    </div>
  );
};

export default VideoPlayer;
