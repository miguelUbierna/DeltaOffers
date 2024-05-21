
using DeltaOffers.Models;
using DeltaOffers.ViewModels;
using MailKit.Security;
using Microsoft.AspNetCore.Http.HttpResults;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using MimeKit;
using MailKit.Net.Smtp;
using System;
using System.Net;
using System.Net.Mime;
using System.Text;
using X.PagedList;
using static System.Runtime.InteropServices.JavaScript.JSType;



namespace DeltaOffers.Controllers
{
    public class UniversidadController : Controller
    {
        private readonly UniversidadesdbContext _context;

        public UniversidadController(UniversidadesdbContext context)
        {
            _context = context;
        }
        [HttpGet("universidad")]
        public IActionResult Index(UniversidadFiltroViewModel filtro)
        {
            ViewData["FiltroFecha"] = filtro.FechaElegida;
            ViewData["FiltroCategoria"] = filtro.Categoria;
            ViewData["FiltroUniversidad"] = filtro.Universidad;

            var query = _context.Universidades.AsQueryable();
            if (filtro.Universidad != null)
            {
                query = query.Where(x => x.UniversidadEspecificada == filtro.Universidad);
            }
            if (filtro.Categoria != null)
            {
                query = query.Where(x => x.Categoria == filtro.Categoria);
            }

            if (filtro.FechaElegida != null)
            {
                DateOnly fechaEnDate = DateOnly.Parse(filtro.FechaElegida);
                query = query.Where(x => x.FechaFin <= fechaEnDate);
            }


            var listadoUbu = query.ToList();

            List<MaestroViewModel> listaRespuesta = new List<MaestroViewModel>();

            foreach (var item in listadoUbu)
            {
                MaestroViewModel respuesta = new MaestroViewModel();
                respuesta.Id = item.Id;
                respuesta.Titulo = item.Titulo;
                respuesta.UniversidadEspecificada = item.UniversidadEspecificada;
                respuesta.Categoria = item.Categoria;
                respuesta.Plazo = item.Plazo;
                respuesta.FechaIni = item.FechaIni;
                respuesta.FechaFin = item.FechaFin;
                respuesta.ImagenLogo = item.ImagenLogo;

                listaRespuesta.Add(respuesta);
            }

            int tamanyoPagina = 10;


            var listaOrdenada = listaRespuesta.OrderByDescending(x => x.FechaFin).ToList();

            filtro.ListaUniversidades = listaOrdenada.ToPagedList(filtro.Pagina, tamanyoPagina);

            return View(filtro);
        }

        [HttpPost]
        public void SendEmail(string email, int ofertaId)
        {

            var archivoAdjunto = GenerarArchivoICS(ofertaId);
            var convocatoria = _context.Universidades.Where(x => x.Id == ofertaId).FirstOrDefault();
            var resumen = "Fin de plazo convocatoria " + convocatoria.Categoria + " " + convocatoria.UniversidadEspecificada;
            var descripcion = convocatoria.Titulo;


            var message = new MimeMessage();
            message.From.Add(new MailboxAddress("Delta Offers", "deltaofferstfg@gmail.com"));
            message.To.Add(new MailboxAddress("", email)); 
            message.Subject = resumen;

            var builder = new BodyBuilder
            {
                TextBody = "Se adjunta en este correo un archivo para añadir a su calendario la siguiente convocatoria: " + convocatoria.Titulo
            };

            byte[] archivo = Encoding.UTF8.GetBytes(archivoAdjunto);
            MemoryStream stream = new MemoryStream(archivo);
            builder.Attachments.Add("Fecha_Fin_Convocatoria.ics", stream );

            message.Body = builder.ToMessageBody();

            using (var client = new SmtpClient())
            {
                client.Connect("smtp.gmail.com", 587, MailKit.Security.SecureSocketOptions.StartTls);
                client.Authenticate("deltaofferstfg@gmail.com", "vtyfdowagyljpuwv");
                client.Send(message); 
                client.Disconnect(true);
            }
            
        }

        private string GenerarArchivoICS(int ofertaId)
        {

            var convocatoria = _context.Universidades.Where(x => x.Id == ofertaId).FirstOrDefault();

            var fecha_fin_inicio = new DateTime(convocatoria.FechaFin.Value.Year, convocatoria.FechaFin.Value.Month, convocatoria.FechaFin.Value.Day, 0, 0, 0);
            var fecha_fin_inicio_formateada = fecha_fin_inicio.ToUniversalTime().ToString("yyyyMMdd'T'HHmmss'Z'");

            var fecha_fin_fin = fecha_fin_inicio.AddHours(24);
            var fecha_fin_fin_formateada = fecha_fin_fin.ToUniversalTime().ToString("yyyyMMdd'T'HHmmss'Z'");

            var resumen = "Fin de plazo convocatoria " + convocatoria.Categoria + " " + convocatoria.UniversidadEspecificada;
            var descripcion = convocatoria.Titulo;


            return $"BEGIN:VCALENDAR\n" +
               $"VERSION:2.0\n" +
               $"BEGIN:VEVENT\n" +
               $"DTSTART:{fecha_fin_inicio_formateada}\n" +
               $"DTEND:{fecha_fin_fin_formateada}\n" +
               $"SUMMARY:{resumen}\n" +
               $"DESCRIPTION:{descripcion}\n" +
               $"END:VEVENT\n" +
               $"END:VCALENDAR";
        }

    }
}