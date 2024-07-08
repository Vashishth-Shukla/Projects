using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.AccessControl;
using System.Text;
using System.Threading.Tasks;

namespace NotesApplication.Commands
{
    internal class UpdateNoteCommand : ICommand
    {
        private readonly AppDbContext _dbContext;
        public UpdateNoteCommand(AppDbContext dbContext)
        {
            _dbContext = dbContext;
        }
        public void Execute()
        {
            Console.WriteLine("Enter the title of the note you wish to update: ");

            var title = Console.ReadLine(); 

            var note = _dbContext.Notes.FirstOrDefault(x => x.Title == title);

            if (note != null)
            {
                Console.WriteLine("Enter the new content : ");
                var newContent = Console.ReadLine();

                note.Content = newContent;

                _dbContext.SaveChanges();

                Console.WriteLine("Note changes were Noted!");
            }
            else
            {
                Console.WriteLine("No note with the given title is previously noted.");

            }
        }
    }
}
