namespace Validator
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Form1));
            this.modPath = new System.Windows.Forms.TextBox();
            this.modLabel = new System.Windows.Forms.Label();
            this.gameLabel = new System.Windows.Forms.Label();
            this.hoi4Path = new System.Windows.Forms.TextBox();
            this.button1 = new System.Windows.Forms.Button();
            this.Doggo = new System.Windows.Forms.PictureBox();
            ((System.ComponentModel.ISupportInitialize)(this.Doggo)).BeginInit();
            this.SuspendLayout();
            // 
            // modPath
            // 
            this.modPath.Location = new System.Drawing.Point(12, 48);
            this.modPath.Name = "modPath";
            this.modPath.Size = new System.Drawing.Size(776, 20);
            this.modPath.TabIndex = 0;
            // 
            // modLabel
            // 
            this.modLabel.AutoSize = true;
            this.modLabel.Location = new System.Drawing.Point(231, 32);
            this.modLabel.Name = "modLabel";
            this.modLabel.Size = new System.Drawing.Size(327, 13);
            this.modLabel.TabIndex = 1;
            this.modLabel.Text = "The path to the folder with the mod you want to run the validator on:";
            this.modLabel.TextAlign = System.Drawing.ContentAlignment.TopCenter;
            // 
            // gameLabel
            // 
            this.gameLabel.AutoSize = true;
            this.gameLabel.Location = new System.Drawing.Point(326, 97);
            this.gameLabel.Name = "gameLabel";
            this.gameLabel.Size = new System.Drawing.Size(141, 13);
            this.gameLabel.TabIndex = 2;
            this.gameLabel.Text = "The path to the HoI4 Folder:";
            // 
            // hoi4Path
            // 
            this.hoi4Path.Location = new System.Drawing.Point(12, 113);
            this.hoi4Path.Name = "hoi4Path";
            this.hoi4Path.Size = new System.Drawing.Size(776, 20);
            this.hoi4Path.TabIndex = 3;
            // 
            // button1
            // 
            this.button1.Location = new System.Drawing.Point(690, 387);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(88, 31);
            this.button1.TabIndex = 4;
            this.button1.Text = "Run Validator";
            this.button1.UseVisualStyleBackColor = true;
            this.button1.Click += new System.EventHandler(this.button1_Click);
            // 
            // Doggo
            // 
            this.Doggo.Image = ((System.Drawing.Image)(resources.GetObject("Doggo.Image")));
            this.Doggo.InitialImage = ((System.Drawing.Image)(resources.GetObject("Doggo.InitialImage")));
            this.Doggo.Location = new System.Drawing.Point(12, 307);
            this.Doggo.Name = "Doggo";
            this.Doggo.Size = new System.Drawing.Size(97, 130);
            this.Doggo.TabIndex = 5;
            this.Doggo.TabStop = false;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(800, 450);
            this.Controls.Add(this.Doggo);
            this.Controls.Add(this.button1);
            this.Controls.Add(this.hoi4Path);
            this.Controls.Add(this.gameLabel);
            this.Controls.Add(this.modLabel);
            this.Controls.Add(this.modPath);
            this.Name = "Form1";
            this.Text = "HoI4 Validator V0.02: Tornado Sucks";
            this.Load += new System.EventHandler(this.Form1_Load);
            ((System.ComponentModel.ISupportInitialize)(this.Doggo)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TextBox modPath;
        private System.Windows.Forms.Label modLabel;
        private System.Windows.Forms.Label gameLabel;
        private System.Windows.Forms.TextBox hoi4Path;
        private System.Windows.Forms.Button button1;
        private System.Windows.Forms.PictureBox Doggo;
    }
}

