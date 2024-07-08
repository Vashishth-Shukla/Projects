namespace NotesApplication.Commands
{
    internal class ReadNoteCommand : ICommand
    {
        private readonly AppDbContext _dbContext;

        public ReadNoteCommand(AppDbContext dbContext)
        {
            _dbContext = dbContext;
        }
        public void Execute()
        {
            Console.WriteLine("Enter the title of the note you wish to read!");
            var title = Console.ReadLine();

            var note = _dbContext.Notes.FirstOrDefault(x => x.Title == title);

            if (note != null)
            {
                Console.WriteLine($"Title:   {note.Title}");
                Console.WriteLine($"Content: {note.Content}");
            }
            else
            {
                Console.WriteLine("No note was found!");
            }

        }
    }
}
