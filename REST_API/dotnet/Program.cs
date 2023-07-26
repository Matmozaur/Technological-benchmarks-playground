var builder = WebApplication.CreateBuilder(args);

// Add services to the container.

builder.Services.AddControllers();

builder.WebHost.ConfigureKestrel(options =>
{
    options.ListenAnyIP(8086);
});

var app = builder.Build();

// Configure the HTTP request pipeline.

app.MapControllers();

app.Run();
