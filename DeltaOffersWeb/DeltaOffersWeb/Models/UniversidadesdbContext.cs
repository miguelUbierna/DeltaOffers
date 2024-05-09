﻿using System;
using System.Collections.Generic;
using Microsoft.EntityFrameworkCore;

namespace DeltaOffers.Models;

public partial class UniversidadesdbContext : DbContext
{
    public UniversidadesdbContext()
    {
    }

    public UniversidadesdbContext(DbContextOptions<UniversidadesdbContext> options)
        : base(options)
    {
    }

    public virtual DbSet<Universidad> Universidades { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Universidad>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("PRIMARY");

            entity.ToTable("universidades");

            entity.Property(e => e.Id).HasColumnName("id");
            entity.Property(e => e.Categoria)
                .HasMaxLength(50)
                .HasColumnName("categoria");
            entity.Property(e => e.Clasificacion)
                .HasMaxLength(50)
                .HasColumnName("clasificacion");
            entity.Property(e => e.Convocante).HasColumnName("convocante");
            entity.Property(e => e.ConvocatoriaAsociada).HasColumnName("convocatoria_asociada");
            entity.Property(e => e.Descripcion).HasColumnName("descripcion");
            entity.Property(e => e.Destinatarios).HasColumnName("destinatarios");
            entity.Property(e => e.Enlace).HasColumnName("enlace");
            entity.Property(e => e.FechaFin)
                .HasColumnType("date")
                .HasColumnName("fecha_fin");
            entity.Property(e => e.FechaIni)
                .HasColumnType("date")
                .HasColumnName("fecha_ini");
            entity.Property(e => e.FechaPublic)
                .HasColumnType("date")
                .HasColumnName("fecha_public");
            entity.Property(e => e.ImagenLogo)
                .HasColumnType("blob")
                .HasColumnName("imagen_logo");
            entity.Property(e => e.NombrePlaza).HasColumnName("nombre_plaza");
            entity.Property(e => e.Plazo)
                .HasMaxLength(50)
                .HasColumnName("plazo");
            entity.Property(e => e.Tipo).HasColumnName("tipo");
            entity.Property(e => e.Titulo).HasColumnName("titulo");
            entity.Property(e => e.UniversidadEspecificada)
                .HasMaxLength(50)
                .HasColumnName("universidad");
        });

        OnModelCreatingPartial(modelBuilder);
    }

    partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
}