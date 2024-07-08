using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace NotesApplication.Commands
{
    internal class DeleteNoteCommand : ICommand
    {
        private readonly AppDbContext _appDbContext;

        public DeleteNoteCommand(AppDbContext appDbContext)
        {
            _appDbContext = appDbContext;
        }

        public void Execute()
        {
            Console.WriteLine("Enter the title of the note you wish to delete: ");
            var title = Console.ReadLine();

            var note = _appDbContext.Notes.FirstOrDefault(x => x.Title == title);

            if (note != null)
            {
                
                _appDbContext.Notes.Remove(note);

                _appDbContext.SaveChanges();

                Console.WriteLine("Note is UnNoted!");
            }
            else
            {
                Console.WriteLine("No note with the given title is previously noted.");

            }
        }
    }
}
