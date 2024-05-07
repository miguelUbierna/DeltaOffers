using DeltaOffers.Models;
using DeltaOffers.ViewModels;
using Microsoft.AspNetCore.Mvc;

namespace DeltaOffers.Controllers
{
    public class DetalleController : Controller
    {
        private readonly UniversidadesdbContext _context;

        public DetalleController(UniversidadesdbContext context)
        {
            _context = context;
        }

        [HttpGet]
        public IActionResult UbuDetalle(int id)
        {

            var convocatoriaDetalle = _context.Universidades.Where(x => x.Id == id).FirstOrDefault();

            UbuViewModel ubuDetalle = new UbuViewModel();

            ubuDetalle.Id = convocatoriaDetalle.Id;
            ubuDetalle.Titulo = convocatoriaDetalle.Titulo;
            ubuDetalle.Plazo = convocatoriaDetalle.Plazo;
            ubuDetalle.UniversidadEspecificada = convocatoriaDetalle.UniversidadEspecificada;
            ubuDetalle.FechaIni = convocatoriaDetalle.FechaIni;
            ubuDetalle.FechaFin = convocatoriaDetalle.FechaFin;
            ubuDetalle.Categoria = convocatoriaDetalle.Categoria;
            ubuDetalle.Enlace = convocatoriaDetalle.Enlace;
            ubuDetalle.Descripcion = convocatoriaDetalle.Descripcion;
            ubuDetalle.FechaPublic = convocatoriaDetalle.FechaPublic;
            ubuDetalle.Convocante = convocatoriaDetalle.Convocante;
            ubuDetalle.Destinatarios = convocatoriaDetalle.Destinatarios;
            ubuDetalle.ImagenLogo = convocatoriaDetalle.ImagenLogo;

            return View(ubuDetalle);
        }


        public IActionResult UleDetalle(int id)
        {

            var convocatoriaDetalle = _context.Universidades.Where(x => x.Id == id).FirstOrDefault();

            UleViewModel uleDetalle = new UleViewModel();

            uleDetalle.Id = convocatoriaDetalle.Id;
            uleDetalle.Titulo = convocatoriaDetalle.Titulo;
            uleDetalle.Plazo = convocatoriaDetalle.Plazo;
            uleDetalle.UniversidadEspecificada = convocatoriaDetalle.UniversidadEspecificada;
            uleDetalle.FechaIni = convocatoriaDetalle.FechaIni;
            uleDetalle.FechaFin = convocatoriaDetalle.FechaFin;
            uleDetalle.Categoria = convocatoriaDetalle.Categoria;
            uleDetalle.Enlace = convocatoriaDetalle.Enlace;
            uleDetalle.Descripcion = convocatoriaDetalle.Descripcion;
            uleDetalle.FechaPublic = convocatoriaDetalle.FechaPublic;
            uleDetalle.NombrePlaza = convocatoriaDetalle.NombrePlaza;
            uleDetalle.Categoria = convocatoriaDetalle.Categoria;
            uleDetalle.Tipo = convocatoriaDetalle.Tipo;
            uleDetalle.ConvocatoriaAsociada= convocatoriaDetalle.ConvocatoriaAsociada;
            uleDetalle.ImagenLogo = convocatoriaDetalle.ImagenLogo;

            return View(uleDetalle);
        }


        [HttpGet]
        public IActionResult UvaDetalle(int id)
        {

            var convocatoriaDetalle = _context.Universidades.Where(x => x.Id == id).FirstOrDefault();

            UvaViewModel uvaDetalle = new UvaViewModel();

            uvaDetalle.Id = convocatoriaDetalle.Id;
            uvaDetalle.Titulo = convocatoriaDetalle.Titulo;
            uvaDetalle.Plazo = convocatoriaDetalle.Plazo;
            uvaDetalle.UniversidadEspecificada = convocatoriaDetalle.UniversidadEspecificada;
            uvaDetalle.FechaIni = convocatoriaDetalle.FechaIni;
            uvaDetalle.FechaFin = convocatoriaDetalle.FechaFin;
            uvaDetalle.Categoria = convocatoriaDetalle.Categoria;
            uvaDetalle.Enlace = convocatoriaDetalle.Enlace;
            uvaDetalle.Categoria = convocatoriaDetalle.Categoria;
            uvaDetalle.Tipo = convocatoriaDetalle.Tipo;
            uvaDetalle.Clasificacion = convocatoriaDetalle.Clasificacion;
            uvaDetalle.ImagenLogo = convocatoriaDetalle.ImagenLogo;

            return View(uvaDetalle);
        }
    }
}
