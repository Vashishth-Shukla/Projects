using System.Runtime.InteropServices;

namespace NotesApplication.Commands
{
    internal class CreateNoteCommand : ICommand
    {
        private readonly AppDbContext _dbContext;

        public CreateNoteCommand(AppDbContext dbContext)
        {
            _dbContext = dbContext;
        }

        public void Execute()
        {
            Console.WriteLine("Please enter the title of your note:");
            var title = Console.ReadLine();

            Console.WriteLine("Add the content of the note:");
            var content = Console.ReadLine();

            var note = new Note()
            {
                Title = title,
                Content = content
            };

            _dbContext.Notes.Add(note);

            _dbContext.SaveChanges();

            Console.WriteLine("Your note is noted!");



        }
    }
}
