// Estado para menú desplegable
// const [showList, setShowList] = useState(true);




import React, { useRef, useState } from "react";
import "../AppLayout.css";




const Sidebar = ({ selected, setSelected, onPreparadoChange }) => {
    const dropRef = useRef(null);
    const [videos, setVideos] = useState([]);
    const [loadingList, setLoadingList] = useState(false);
    const [uploading, setUploading] = useState(false);

    // Cargar la lista de videos al montar el componente
    React.useEffect(() => {
        const fetchVideos = async () => {
            setLoadingList(true);
            try {
                const res = await fetch("http://localhost:8000/videos_disponibles/");
                if (res.ok) {
                    const data = await res.json();
                    setVideos(data.videos);
                    // No seleccionar ningún video automáticamente
                } else {
                    setVideos([]);
                }
            } catch (err) {
                setVideos([]);
            }
            setLoadingList(false);
        };
        fetchVideos();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    const handleDragOver = (e) => {
        e.preventDefault();
        dropRef.current.classList.add("drag-over");
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        dropRef.current.classList.remove("drag-over");
    };


    const fileInputRef = useRef(null);

    const uploadFiles = async (files) => {
        const videoFiles = Array.from(files).filter(f => f.type.startsWith("video/"));
        if (videoFiles.length === 0) {
            alert("Por favor, selecciona solo archivos de video.");
            return;
        }
        setUploading(true);
        for (const file of videoFiles) {
            const formData = new FormData();
            formData.append("file", file);
            try {
                const res = await fetch("http://localhost:8000/upload-video/", {
                    method: "POST",
                    body: formData
                });
                if (res.ok) {
                    setVideos((prev) => [...prev, file.name]);
                } else {
                    const data = await res.json();
                    alert(data.error || "Error subiendo el video");
                }
            } catch (err) {
                alert("Error de red subiendo el video");
            }
        }
        setUploading(false);
    };

    const handleDrop = async (e) => {
        e.preventDefault();
        dropRef.current.classList.remove("drag-over");
        await uploadFiles(e.dataTransfer.files);
    };

    const handleClickDrop = () => {
        if (fileInputRef.current) fileInputRef.current.click();
    };

    const handleFileChange = (e) => {
        uploadFiles(e.target.files);
        e.target.value = ""; // reset para permitir subir el mismo archivo de nuevo
    };

    // Recargar lista de videos desde el backend
    const handleReload = async () => {
        setLoadingList(true);
        try {
            const res = await fetch("http://localhost:8000/videos_disponibles/");
            if (res.ok) {
                const data = await res.json();
                setVideos(data.videos);
                // Si el video seleccionado ya no existe, deselecciona
                if (!data.videos.includes(selected)) {
                    setSelected(null);
                }
            } else {
                alert("Error recargando la lista de videos");
            }
        } catch (err) {
            alert("Error de red recargando la lista de videos");
        }
        setLoadingList(false);
    };

    // Estado para carga de modelo Whisper

    // Estado para los recursos del video seleccionado
    const [videoStatus, setVideoStatus] = useState({ audio: false, transcript: false, embeddings: false });
    const [checkingStatus, setCheckingStatus] = useState(false);

    // Consultar el estado de los recursos del video seleccionado
    React.useEffect(() => {
        if (!selected) return;
        const nombreSinExtension = selected.replace(/\.[^/.]+$/, "");
        setCheckingStatus(true);
        fetch(`http://localhost:8000/video_status/${encodeURIComponent(nombreSinExtension)}`)
            .then(res => res.ok ? res.json() : { audio: false, transcript: false, embeddings: false })
            .then(data => {
                setVideoStatus({
                    audio: !!data.audio,
                    transcript: !!data.transcript,
                    embeddings: !!data.embeddings
                });
                setCheckingStatus(false);
            })
            .catch(() => {
                setVideoStatus({ audio: false, transcript: false, embeddings: false });
                setCheckingStatus(false);
            });
    }, [selected]);


    const allReady = videoStatus.audio && videoStatus.transcript && videoStatus.embeddings;
    // Avisar al padre cuando cambia el estado de preparado
    React.useEffect(() => {
        if (typeof onPreparadoChange === 'function') {
            onPreparadoChange(allReady);
        }
        // eslint-disable-next-line
    }, [allReady]);

    // Handler para el botón de preprocesar
    const [preprocessing, setPreprocessing] = useState(false);
    const handlePreprocesar = async () => {
        if (!selected) return;
        setPreprocessing(true);
        try {
            const res = await fetch(`http://localhost:8000/preprocess-video/${encodeURIComponent(selected)}`, {
                method: 'POST'
            });
            if (res.ok) {
                // Actualizar estado tras preprocesar
                setTimeout(() => {
                    // Espera breve para que el backend termine de guardar archivos
                    setCheckingStatus(true);
                    fetch(`http://localhost:8000/video_status/${encodeURIComponent(selected.replace(/\.[^/.]+$/, ""))}`)
                        .then(res => res.ok ? res.json() : { audio: false, transcript: false, embeddings: false })
                        .then(data => {
                            setVideoStatus({
                                audio: !!data.audio,
                                transcript: !!data.transcript,
                                embeddings: !!data.embeddings
                            });
                            setCheckingStatus(false);
                        })
                        .catch(() => {
                            setVideoStatus({ audio: false, transcript: false, embeddings: false });
                            setCheckingStatus(false);
                        });
                }, 800);
            } else {
                const data = await res.json();
                alert(data.error || 'Error en el preprocesado');
            }
        } catch (err) {
            alert('Error de red en el preprocesado');
        }
        setPreprocessing(false);
    };

    return (
        <div className="sidebar sidebar-modern">
            <h2 className="sidebar-title">Importar videos</h2>
            <div
                ref={dropRef}
                className="drop-zone drop-zone-modern"
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={handleClickDrop}
                style={{ cursor: uploading ? "not-allowed" : "pointer", pointerEvents: uploading ? "none" : "auto" }}
            >
                <input
                    ref={fileInputRef}
                    type="file"
                    accept="video/*"
                    multiple
                    style={{ display: "none" }}
                    onChange={handleFileChange}
                />
                <span className="drop-zone-main">Arrastra y suelta tus videos aquí</span>
                <span className="drop-zone-sub">o haz click para seleccionar</span>
                {uploading && <span className="drop-zone-uploading">Subiendo...</span>}
            </div>

            <div className="video-list video-list-modern">
                <div className="video-list-header" >
                    <h3 className="video-list-title" style={{ margin: 0 }}>Videos disponibles</h3>
                    <button
                        onClick={handleReload}
                        className="video-list-reload"
                        disabled={loadingList}
                        title="Recargar lista de videos"
                        style={{ marginLeft: "8px" }}
                    >
                        {loadingList ? "..." : "⟳"}
                    </button>
                </div>

                <ul className="video-list-ul">
                    {videos.length === 0 ? (
                        <li style={{ color: '#888', fontWeight: 500, fontSize: 16, textAlign: 'center', marginBottom: '1.2em' }}>
                            No se han subido videos aún
                        </li>
                    ) : (
                        videos.map((video) => {
                            const isSelected = selected === video;
                            return (
                                <li
                                    className={`video-list-item-custom${isSelected ? " selected" : ""}`}
                                    key={video}
                                    onClick={() => setSelected(video)}
                                >
                                    <span>{video}</span>
                                </li>
                            );
                        })
                    )}
                </ul>
            </div>

            {/* Estado de procesamiento del video seleccionado */}
            {selected ? (
                <div className="video-status-panel">
                    <div className="video-status-header">
                        <span className="video-status-title">{selected}</span>
                    </div>
                    <ul className="video-status-list">
                        <li className="video-status-item">
                            <span className={`video-status-dot ${videoStatus.audio ? 'ok' : 'fail'}`}>{videoStatus.audio ? '✔' : '✖'}</span>
                            <span>Audio extraído</span>
                        </li>
                        <li className="video-status-item">
                            <span className={`video-status-dot ${videoStatus.transcript ? 'ok' : 'fail'}`}>{videoStatus.transcript ? '✔' : '✖'}</span>
                            <span>Transcripción</span>
                        </li>
                        <li className="video-status-item">
                            <span className={`video-status-dot ${videoStatus.embeddings ? 'ok' : 'fail'}`}>{videoStatus.embeddings ? '✔' : '✖'}</span>
                            <span>Embeddings</span>
                        </li>
                    </ul>
                    <div className="video-status-actions">
                        <button
                            onClick={handlePreprocesar}
                            disabled={allReady || preprocessing}
                            className={`video-status-preprocess-btn${allReady ? ' prepared' : ''}`}
                        >
                            {allReady
                                ? 'Preparado'
                                : (preprocessing ? 'Preprocesando...' : 'Preprocesar')}
                        </button>
                    </div>
                </div>
            ) : (
                <div className="video-status-panel video-status-empty">
                    No hay video seleccionado
                </div>
            )}
        </div>
    );
};

export default Sidebar;
