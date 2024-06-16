using System;
using System.Windows;
using System.Windows.Input;

namespace AreYouDubm
{
    public partial class MainWindow : Window
    {
        bool tryagain = false;
        Random random = new Random();

        public MainWindow()
        {
            InitializeComponent();
        }

        private void YesButton_Click(object sender, RoutedEventArgs e)
        {
            if (tryagain)
            {
                Text.Text = "Are you dumb?";
                YesButton.Content = "Yes!";
            }
            else
            {
                Text.Text = "Ohh! Well who isn't?";
                YesButton.Content = "Try Again";
            }
            tryagain = !tryagain;
        }

        private void Window_MouseMove(object sender, MouseEventArgs e)
        {
            var mousePos = e.GetPosition(this);
            var buttonPos = NoButton.TransformToAncestor(this).Transform(new Point(0, 0));
            var buttonSize = new Size(NoButton.ActualWidth, NoButton.ActualHeight);

            if (IsMouseOverButton(buttonPos, buttonSize, mousePos))
            {
                double newX, newY;
                do
                {
                    newX = random.Next(0, (int)(this.ActualWidth - NoButton.ActualWidth));
                    newY = random.Next(0, (int)(this.ActualHeight - NoButton.ActualHeight));
                } while (IsMouseOverButton(new Point(newX, newY), buttonSize, mousePos));

                NoButton.Margin = new Thickness(newX, newY, 0, 0);
            }
        }

        private bool IsMouseOverButton(Point buttonPos, Size buttonSize, Point mousePos)
        {
            return mousePos.X >= buttonPos.X && mousePos.X <= buttonPos.X + buttonSize.Width &&
                   mousePos.Y >= buttonPos.Y && mousePos.Y <= buttonPos.Y + buttonSize.Height;
        }
    }
}
