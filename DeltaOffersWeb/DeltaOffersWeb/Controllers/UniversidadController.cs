
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
using System.Globalization;
using Mysqlx.Cursor;



namespace DeltaOffers.Controllers
{
    public class UniversidadController : Controller
    {
        private readonly ConvocatoriasdbContext _context;
        
        public UniversidadController(ConvocatoriasdbContext context)
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
                DateOnly fechaEnDate = DateOnly.ParseExact(filtro.FechaElegida, "dd/MM/yyyy", CultureInfo.InvariantCulture);
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
                var fechaStringIni= string.Format("{0:dd/MM/yyyy}", item.FechaIni); 
                respuesta.FechaIniString = fechaStringIni;
                var fechaStringFin = string.Format("{0:dd/MM/yyyy}", item.FechaFin);
                respuesta.FechaFinString = fechaStringFin;
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
                TextBody = "DeltaOffers Informa: \n\nSe adjunta en este correo un archivo para añadir a su calendario la fecha de finalización de siguiente convocatoria: \n" 
                + convocatoria.Titulo + "\n" +
                "Puedes acceder a ella mediante el siguiente enlace: " + convocatoria.Enlace
                + "\n\nEquipo de DeltaOffers."
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

            var zonaHoraria = TimeZoneInfo.FindSystemTimeZoneById("Central European Standard Time");
            
            var fecha_fin_inicio = new DateTime(convocatoria.FechaFin.Value.Year, convocatoria.FechaFin.Value.Month, convocatoria.FechaFin.Value.Day, 0, 0, 0);
            var fechaFinInicioEnZonaHoraria = TimeZoneInfo.ConvertTimeToUtc(fecha_fin_inicio, zonaHoraria);
            var fecha_fin_inicio_formateada = fechaFinInicioEnZonaHoraria.ToUniversalTime().ToString("yyyyMMdd'T'HHmmss'Z'");

            var fecha_fin_fin = fecha_fin_inicio.AddHours(24);
            var fechaFinFinEnZonaHoraria = TimeZoneInfo.ConvertTimeToUtc(fecha_fin_fin, zonaHoraria);
            var fecha_fin_fin_formateada = fechaFinFinEnZonaHoraria.ToUniversalTime().ToString("yyyyMMdd'T'HHmmss'Z'");

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