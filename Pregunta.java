import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

public class Pregunta implements Publicacion {
    private String titulo;
    private String cuerpo;
    private LocalDate fechaPublicacion;
    private List<Respuesta> respuestas;

    public Pregunta(String titulo, String cuerpo, LocalDate fechaPublicacion) {
        this.titulo = titulo;
        this.cuerpo = cuerpo;
        this.fechaPublicacion = fechaPublicacion;
        this.respuestas = new ArrayList<>();
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

    // Getters, Setters y métodos adicionales
    public String getTitulo() {
        return titulo;
    }

    public void setTitulo(String titulo) {
        this.titulo = titulo;
    }

    public void setCuerpo(String cuerpo) {
        this.cuerpo = cuerpo;
    }

    public void setFechaPublicacion(LocalDate fechaPublicacion) {
        this.fechaPublicacion = fechaPublicacion;
    }

    public List<Respuesta> getRespuestas() {
        return respuestas;
    }

    public void agregarRespuesta(Respuesta respuesta) {
        this.respuestas.add(respuesta);
    }
}