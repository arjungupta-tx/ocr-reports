prompt_for_merge_document=""" 
I have three OCR outputs from the same document. Each OCR result may have missing sentences, incorrect text, or variations in formatting. 
I want you to analyze the three versions and create one perfect document by combining all the accurate and missing content.


   Here are the documents:

    1. Document 1:
    {doc1}

    2. Document 2:
    {doc2}

    3. Document 3:
    {doc3}

 Your task is to:
    - Identify missing sentences or text in any of the documents.
    - Resolve inconsistencies or differences.
    - Combine all the content into one coherent, accurate document.
    - Ensure that the final document is well-formatted and complete.

    Please return the merged document. Nothing else.


"""