// Formatea segundos a hh:mm:ss
  function formatTime(secs) {
    const s = Math.floor(secs % 60).toString().padStart(2, '0');
    const m = Math.floor((secs / 60) % 60).toString().padStart(2, '0');
    const h = Math.floor(secs / 3600).toString();
    return h !== '0' ? `${h}:${m}:${s}` : `${m}:${s}`;
  }
import React, { useState } from "react";
import "../AppLayout.css";

// Se espera que el nombre del video esté disponible como prop
const Consulta = ({ consultaHabilitada, selectedVideo, onClipsChange }) => {
  const [query, setQuery] = useState("");
  const [topK, setTopK] = useState(5);
  const [clips, setClips] = useState([]);
  const [loading, setLoading] = useState(false);
  const [clipLength, setClipLength] = useState(30); // segundos
  const [selectedClip, setSelectedClip] = useState(null);

  // Notificar a App.jsx si hay clips
  React.useEffect(() => {
    if (onClipsChange) onClipsChange(clips.length > 0);
  }, [clips, onClipsChange]);

  const handleBuscar = async () => {
    if (!consultaHabilitada) return;
    if (!query.trim()) return;
    if (!selectedVideo) return;
    setLoading(true);
    setClips([]);
    setSelectedClip(null); // Cierra el modal si está abierto
    // Genera un parámetro único para esta búsqueda
    const uniqueParam = Date.now();
    try {
      // 1. POST para generar clips y metadatos
      const res = await fetch(`http://localhost:8000/video_search/${encodeURIComponent(selectedVideo)}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query,
          top_k: topK,
          clip_length: clipLength
        })
      });
      if (!res.ok) throw new Error("Error en la generación de clips");
      // 2. GET para obtener los metadatos (estructura plana)
      const videoBase = selectedVideo.endsWith('.mp4') ? selectedVideo.slice(0, -4) : selectedVideo;
      // Para evitar caché de thumbnails antiguos, añade un parámetro único
      const metaRes = await fetch(`http://localhost:8000/clips_metadata/${encodeURIComponent(videoBase)}?t=${uniqueParam}`);
      if (!metaRes.ok) throw new Error("Error obteniendo metadatos de clips");
      const data = await metaRes.json();
      if (data.results && Array.isArray(data.results)) {
        setClips(
          data.results.map((clip, idx) => {
            const thumbUrl = clip.thumbnail_url ? (clip.thumbnail_url.startsWith('http') ? clip.thumbnail_url : `http://localhost:8000${clip.thumbnail_url}`) : null;
            const videoUrl = clip.clip_url.startsWith('http') ? clip.clip_url : `http://localhost:8000${clip.clip_url}`;
            return {
              id: clip.clip_id !== undefined ? clip.clip_id : idx,
              url: videoUrl + `?t=${uniqueParam}`,
              start: clip.start,
              end: clip.end,
              score: clip.score,
              thumbnail: thumbUrl ? (thumbUrl + `?t=${uniqueParam}`) : null
            };
          })
        );
      } else {
        setClips([]);
      }
    } catch (e) {
      console.log('Error en fetch:', e);
      setClips([]);
    }
    setLoading(false);

  };

  return (
    <div className="consulta">
      <h2 className="consulta-title">Encuentra los momentos que más te interesan del video</h2>
      <div className="consulta-bar">
        <input
          type="text"
          className="consulta-query-input"
          placeholder="Ejemplos: Eva comió la manzana porque"
          value={query}
          onChange={e => setQuery(e.target.value)}
          disabled={!consultaHabilitada || loading}
          onKeyDown={e => { if (e.key === 'Enter') handleBuscar(); }}
        />
        <button
          className={`consulta-buscar-btn${consultaHabilitada && query.trim() && !loading ? '' : ' consulta-buscar-btn-disabled'}`}
          onClick={() => handleBuscar()}
          disabled={!consultaHabilitada || loading || !query.trim()}
        >
          <span role="img" aria-label="Buscar" className="consulta-buscar-icon">🔍</span>
          {loading ? 'Buscando...' : 'Buscar'}
        </button>
        <button
          className="consulta-clear-btn"
          onClick={() => {
            setQuery("");
            setClips([]);
            setSelectedClip(null);
          }}
          disabled={!consultaHabilitada && !query && clips.length === 0}
          title="Limpiar búsqueda"
        >
          Limpiar
        </button>
      </div>

      {/* Sliders de parámetros */}
      <div className="consulta-sliders">
        <div className="consulta-slider-group">
          <label htmlFor="topk-slider" className="consulta-slider-label">Top K: <b>{topK}</b></label>
          <input
            id="topk-slider"
            type="range"
            min={1}
            max={10}
            value={topK}
            disabled={!consultaHabilitada}
            onChange={e => setTopK(Number(e.target.value))}
            className="consulta-slider"
          />
        </div>
        <div className="consulta-slider-group">
          <label htmlFor="cliplength-slider" className="consulta-slider-label">Longitud de clip (segundos): <b>{clipLength}</b></label>
          <input
            id="cliplength-slider"
            type="range"
            min={20}
            max={120}
            value={clipLength}
            disabled={!consultaHabilitada}
            onChange={e => setClipLength(Number(e.target.value))}
            className="consulta-slider"
          />
        </div>
      </div>
      {(!loading && clips.length > 0) && (
        <div>
          Clips más relevantes para <b>{query ? `"${query}"` : ""}</b>:
        </div>
      )}
      {/* Grid clásico de clips */}
      <div className="consulta-clips-grid">
        {loading && (
          <div className="consulta-clips-loading">Buscando clips...</div>
        )}
        {!loading && clips.length === 0 && consultaHabilitada && (
          <div className="consulta-clips-empty">No hay resultados aún. Realiza una consulta.</div>
        )}
        {!loading && clips.length > 0 && (
          <div className="consulta-clips-grid-inner">
            {clips.map((clip, idx) => (
              <div
                key={clip.id}
                className="consulta-clip-card consulta-clip-card-horizontal"
                style={{
                  backgroundImage: clip.thumbnail ? `url('${clip.thumbnail}')` : undefined,
                  backgroundSize: 'cover',
                  backgroundPosition: 'center',
                  backgroundColor: '#e3f2fd',
                  position: 'relative',
                  cursor: 'pointer',
                  minWidth: 0,
                }}
                onClick={() => setSelectedClip(clip)}
              >
                {/* Overlay para legibilidad */}
                <div style={{
                  position: 'absolute',
                  left: 0, top: 0, right: 0, bottom: 0,
                  background: 'linear-gradient(180deg, rgba(20,40,80,0.22) 0%, rgba(20,40,80,0.32) 60%, rgba(20,40,80,0.44) 100%)',
                  zIndex: 1,
                  pointerEvents: 'none',
                }} />
                <div className="consulta-clip-info" style={{ position: 'absolute', left: 0, right: 0, top: 0, zIndex: 2, display: 'flex', flexDirection: 'column', alignItems: 'flex-start', gap: 7, padding: '13px 15px 0 15px', width: '100%', pointerEvents: 'none' }}>
                  <div className="consulta-clip-score">
                    <b>Relevancia:</b> {clip.score !== undefined ? Number(clip.score).toFixed(3) : 'N/A'}
                  </div>
                  <div className="consulta-clip-time">
                    {`${formatTime(clip.start)} - ${formatTime(clip.end)}`}
                  </div>
                </div>
                {!clip.thumbnail && (
                  <div style={{ position: 'absolute', left: 0, top: 0, width: '100%', height: '100%', background: '#eee', color: '#1976d2', fontWeight: 600, display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 0 }}>
                    Sin thumbnail
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Modal de clip expandido */}
      {selectedClip && (
        <div className="consulta-clip-modal-overlay" onClick={() => setSelectedClip(null)}>
          <div
            className="consulta-clip-modal"
            onClick={e => e.stopPropagation()}
          >
            <button
              className="consulta-clip-modal-close"
              onClick={() => setSelectedClip(null)}
              aria-label="Cerrar"
            >
              ×
            </button>
            <video
              src={selectedClip.url}
              controls
              className="consulta-clip-modal-video"
              autoPlay
              preload="metadata"
              style={{ width: '100%', maxHeight: '70vh', borderRadius: 12 }}
            />
            <div className="consulta-clip-modal-info">
              <div className="consulta-clip-modal-info-score">
                <b>Relevancia:</b> {selectedClip.score !== undefined ? Number(selectedClip.score).toFixed(3) : 'N/A'}
              </div>
              <div className="consulta-clip-modal-info-time">
                {`${formatTime(selectedClip.start)} - ${formatTime(selectedClip.end)}`}
              </div>
            </div>
          </div>
        </div>
      )}

      {!consultaHabilitada && (
        <div style={{ color: '#888', fontWeight: 500, fontSize: 16, marginTop: 12 }}>
          Debes preparar el video antes de consultar.
        </div>
      )}
    </div>
  );
};

export default Consulta;
