using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Mvc;

namespace DeltaOffers.Controllers
{
    public class AccountController : Controller
    {
        public IActionResult Login()
        {
            var autenticacion = new AuthenticationProperties
            {
                RedirectUri = Url.Action("LoginRespuesta", "Account")
            };

            return Challenge(autenticacion, "Google");
        }

        public async Task<IActionResult> LoginRespuesta() {

            var respuestaAutenticacion = await HttpContext.AuthenticateAsync();
            if (!respuestaAutenticacion.Succeeded)
            {
                return RedirectToAction("Login");
            }
            else
            {
                return RedirectToAction("Index", "Home");
            }
 
        }

        public async Task<IActionResult> Logout()
        {
            await HttpContext.SignOutAsync();

            return RedirectToAction("Index", "Home");
        }
    }
}
