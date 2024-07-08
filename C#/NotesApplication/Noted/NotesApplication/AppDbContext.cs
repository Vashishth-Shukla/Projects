using Microsoft.EntityFrameworkCore;

namespace NotesApplication
{
    internal class AppDbContext :DbContext
    {
        public  DbSet<Note> Notes { get; set; }
        public string DbPath { get; }

        public AppDbContext()
        {
            var folder = Environment.SpecialFolder.LocalApplicationData;
            var path = Environment.GetFolderPath(folder);

            DbPath = Path.Join(path, "Notes.db");

        }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder) =>
            optionsBuilder.UseSqlite($"Data Source = {DbPath}");
    }
}
