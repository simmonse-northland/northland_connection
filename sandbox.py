    # this works just probably dont need it 

    # @classmethod
    # def split_pdf(cls, directory):
    #     files = os.listdir(directory)
    #     for file in files:
    #         if file.endswith('.pdf'):
    #             pdf_path = os.path.join(directory, file)
    #             with open(pdf_path, 'rb') as pdf_file:
    #                 pdf_reader = PdfReader(pdf_file)
    #                 num_pages = len(pdf_reader.pages)
                    
    #                 if num_pages > 1:
    #                     for page_num in range(num_pages):
    #                         new_filename = os.path.splitext(file)[0] + f'_page{page_num+1}.pdf'
    #                         pdf_writer = PdfWriter()
    #                         pdf_writer.add_page(pdf_reader.pages[page_num])
    #                         pdf_writer.write(os.path.join(directory, new_filename))
    #                     pdf_file.close()
    #                     os.remove(pdf_path)
    #                     print(f"File {pdf_path} has been split into {num_pages} pages.")
    #                 else:
    #                     print(f"File {pdf_path} has only 1 page, no need to split.")