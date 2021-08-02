sudo apt-get install -y texlive

# if you have 5GB and a lot of buildtime to spare you can replace the next texlive packages with
# sudo apt-get install -y texlive-full
sudo apt-get install -y texlive-extra
sudo apt-get install -y texlive-science
sudo apt-get install -y texlive-latex-extra
sudo apt-get install -y texlive-fonts-extra

# Required for pdfinfo and pdffonts
sudo apt-get install -y poppler-utils
