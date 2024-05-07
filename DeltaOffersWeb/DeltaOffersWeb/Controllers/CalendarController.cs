using Google.Apis.Auth.OAuth2;
using Google.Apis.Calendar.v3.Data;
using Google.Apis.Calendar.v3;
using Google.Apis.Services;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using DeltaOffers.Models;
using DeltaOffers.ViewModels;

namespace DeltaOffers.Controllers
{
    public class CalendarController : Controller
    {
        private readonly UniversidadesdbContext _context;

        public CalendarController(UniversidadesdbContext context)
        {
            _context = context;
        }

        public async Task<IActionResult> CrearEvento(int id)
        {
            var usuarioAutenticado = await HttpContext.AuthenticateAsync();
            if (!usuarioAutenticado.Succeeded)
            {
                return Unauthorized();
            }

            var tokenUsuario = usuarioAutenticado.Properties.GetTokenValue("access_token");

            
            var initializer = new BaseClientService.Initializer
            {
                HttpClientInitializer = GoogleCredential.FromAccessToken(tokenUsuario),
                ApplicationName = "DeltaOffers"
            };

            var calendarService = new CalendarService(initializer);

            var convocatoria = _context.Universidades.Where(x => x.Id == id).FirstOrDefault();

            var fecha_fin = new DateTime(convocatoria.FechaFin.Value.Year,convocatoria.FechaFin.Value.Month,convocatoria.FechaFin.Value.Day,0, 0, 0);

            
            var newEvent = new Event
            {
                Summary = "Fin de plazo convocatoria "+ convocatoria.Categoria +" "+ convocatoria.UniversidadEspecificada,
                Description = convocatoria.Titulo,
                Start = new EventDateTime { DateTime = fecha_fin },
                End = new EventDateTime { DateTime = fecha_fin.AddHours(24)}
            };

            var calendarId = "primary";

            await calendarService.Events.Insert(newEvent, calendarId).ExecuteAsync();

            return RedirectToAction("Index", "Universidad");
        }
    }
}
