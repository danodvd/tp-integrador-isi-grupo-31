import java.time.LocalDate;

public class Respuesta implements Publicacion {
    private Boolean aceptado;
    private Integer id_autor;
    private String cuerpo;
    private LocalDate fechaPublicacion;
    private Pregunta pregunta; // Relación 0..* a 1 con Pregunta

    public Respuesta(Boolean aceptado, Integer id_autor, String cuerpo, LocalDate fechaPublicacion, Pregunta pregunta) {
        this.aceptado = aceptado;
        this.id_autor = id_autor;
        this.cuerpo = cuerpo;
        this.fechaPublicacion = fechaPublicacion;
        this.pregunta = pregunta;
    }

    // Métodos de la interfaz Publicacion
    @Override
    public String getCuerpo() {
        return this.cuerpo;
    }

    @Override
    public LocalDate getFechaPublicacion() {
        return this.fechaPublicacion;
    }

    // Getters y Setters
    public Boolean getAceptado() {
        return aceptado;
    }

    public void setAceptado(Boolean aceptado) {
        this.aceptado = aceptado;
    }

    public Integer getId_autor() {
        return id_autor;
    }

    public void setId_autor(Integer id_autor) {
        this.id_autor = id_autor;
    }

    public void setCuerpo(String cuerpo) {
        this.cuerpo = cuerpo;
    }

    public void setFechaPublicacion(LocalDate fechaPublicacion) {
        this.fechaPublicacion = fechaPublicacion;
    }

    public Pregunta getPregunta() {
        return pregunta;
    }

    public void setPregunta(Pregunta pregunta) {
        this.pregunta = pregunta;
    }
}