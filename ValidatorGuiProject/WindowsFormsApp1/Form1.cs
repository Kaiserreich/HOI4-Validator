using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Diagnostics;

namespace Validator
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            string fModPath, fHoi4Path;
            fModPath = modPath.Text;
            fHoi4Path = hoi4Path.Text;
            Process cmd = new Process();
            cmd.StartInfo = new ProcessStartInfo();
            cmd.StartInfo.WindowStyle = ProcessWindowStyle.Hidden;
            cmd.StartInfo.FileName = "cmd.exe";
            cmd.StartInfo.Arguments = "/C " + "validator.exe --" + fModPath + " --" + fHoi4Path;
            cmd.Start();
            cmd.WaitForExit();
            MessageBox.Show("Validator finished, output should be in the same directory as this program!", this.Text);
            Application.Exit();
        }
    }
}
