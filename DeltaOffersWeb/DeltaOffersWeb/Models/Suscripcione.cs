using System;
using System.Collections.Generic;

namespace DeltaOffers.Models;

public partial class Suscripcion
{
    public int Id { get; set; }

    public string Email { get; set; } = null!;

    public int? NumAvisos { get; set; }
}
