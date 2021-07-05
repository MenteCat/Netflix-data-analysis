# Netflix-data-analysis

Tested on Python 3.8.

How to use:

.. code-block:: python

    pip install pandas matplotlib

.. code-block:: python

    from netflix_analysis import cleanup, filtering_data, calculation

    clean_data = cleanup('ViewingActivity.csv')
    filtered_data = filtering_data(clean_data)
    
    calculation(filtered_data)

The results will be printed on screen (and graphs will show if you have matplotlib installed).