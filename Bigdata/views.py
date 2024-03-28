from django.shortcuts import render
from pymongo import ASCENDING, DESCENDING, MongoClient
import pymongo
from django.views.decorators.csrf import csrf_exempt


def home(request):
     return render(request,'index.html')
def insert(request):
     return render(request,'insert.html')
def delete(request):
     return render(request,'delete.html')
def quires(request):
     return render(request,'quires.html')
def result(request):
      return render(request,'result.html')


def insertOneInStructuralP1(request):
    # create a MongoClient instance
    client = MongoClient(host='localhost', port=27017)
    # connect to the database
    Pdb = client.get_database('PDB') 
    # get a reference to the collection
    collection1 = Pdb.get_collection("structuralP1")
    # create a dictionary from the HTTP POST request data
    inputDictWeb = {
        "_id": request.POST.get('input1', ''),
        "classification": request.POST.get('input2', ''),
        "experimentalTechnique": request.POST.get('input3', ''),
        "macromoleculeType": request.POST.get('input4', ''),
        "residueCount": request.POST.get('input5', ''),
        "resolution": request.POST.get('input6', ''),
        "structureMolecularWeight": request.POST.get('input7', ''),
        "phValue": request.POST.get('input8', ''),
        "publicationYear": request.POST.get('input9', ''),
    }
    # insert the document into the collection
    result = collection1.insert_one(inputDictWeb)

    # return an HTTP response indicating success or failure
    if result:
            context = {'message': 'Document inserted successfully'}
    else:
            context = {'message': 'Error in inserting document'}
    return render(request, 'inserted.html', context)


@csrf_exempt
def delete_from_mongodb(request):
        if request.method == 'POST':
        # Connect to the MongoDB database
        # create a MongoClient instance
           client = MongoClient(host='localhost', port=27017)
        # connect to the database
        Pdb = client.get_database('PDB')
        # get a reference to the collection
        collection1 = Pdb.get_collection("structuralP1")
        # Extract the ID from the form data
        id = request.POST.get('input1')
        # Delete the document from the collection
        result = collection1.delete_one({'_id': id})

        # Render the delete.html template with the response message
        if result.deleted_count == 1:
            context = {'message': 'Document deleted successfully'}
        else:
            context = {'message': 'Document not found'}
        return render(request, 'deleted.html', context)

    # if request.method == 'POST':
    #     # Connect to the MongoDB database
    #     # create a MongoClient instance
    #     client = MongoClient(host='localhost', port=27017)
    #     # connect to the database
    #     Pdb = client.get_database('PDB') 
    #     # get a reference to the collection
    #     collection1 = Pdb.get_collection("structuralP1")
    #     # Extract the ID from the form data
    #     id = request.POST.get('input1')
    #     # Delete the document from the collection
    #     result = collection1.delete_one({'_id': id})

    #     # Return a JSON response with the status of the operation
    #     if result.deleted_count == 1:
    #         return HttpResponse("Document deleted successfully")
    #     else:
    #         return HttpResponse("Document not found")

#get_ALKALIN proteins
def result1(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB') 
    collection1 = Pdb.get_collection("structuralP1")

    # Execute the query
    docs_ph_alkaline = collection1.find({"phValue": {"$gt": 7}})

    # Pass the results to the template
    context = {"docs_ph_alkaline": docs_ph_alkaline}
    return render(request, "result.html", context)

#GET ALL DOCUMENTS
def result2(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB') 
    collection1 = Pdb.get_collection("structuralP1")

    # Execute the query
    all_docs = collection1.find()

    # Add the query results to the context dictionary
    context = {"all_docs": all_docs}

    # Render the template with the context dictionary
    return render(request, "result2.html", context)    

# get acidik proteins 

def result3(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB') 
    collection1 = Pdb.get_collection("structuralP1")

    # Define the aggregation pipeline
    pipeline = [
        {
            "$match": {
                "phValue": {"$lt": 7}
            }
        }
    ]

    # Execute the aggregation pipeline query
    docs_ph_acidic = collection1.aggregate(pipeline)

    # Add the query results to the context dictionary
    context = {"docs_ph_acidic": docs_ph_acidic}

    # Render the template with the context dictionary
    return render(request, "result3.html", context)

#Getting large macromolecular complexes
def result4(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB') 
    collection1 = Pdb.get_collection("structuralP1")

    # Execute the aggregation pipeline
    pipeline = [
        {"$match": {"residueCount": {"$gt": 100}}}
    ]
    docs_complex_residues = collection1.aggregate(pipeline)

    # Render the template with the query results
    return render(request, "result4.html", {"docs_complex_residues": docs_complex_residues})


#Getting large Protein macromolecular complexes
def result5(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB') 
    collection1 = Pdb.get_collection("structuralP1")

    # Execute the query
    docs_Complex_protein = collection1.find({"$and":[{"residueCount":{"$gt":100}},{"macromoleculeType":"Protein"}]})

    # Add the query results to the context dictionary
    context = {"docs_Complex_protein": docs_Complex_protein}

    # Render the template with the context dictionary
    return render(request, "result5.html", context)

#Getting average resolution of Data
def result6(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB') 
    collection1 = Pdb.get_collection("structuralP1")

    # Define the aggregation pipeline
    pipeline = [
        {
            "$group": {
                "_id": None,
                "average_resolution_value": {"$avg": "$resolution"}
            }
        }
    ]

    # Execute the aggregation pipeline query
    AvgRes = collection1.aggregate(pipeline)

    # Extract the query result
    average_value = AvgRes.next()["average_resolution_value"]

    # Add the query result to the context dictionary
    context = {"average_value": average_value}

    # Render the template with the context dictionary
    return render(request, "result6.html", context)

#Getting Data with No phValue
def result7(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB') 
    collection1 = Pdb.get_collection("structuralP1")

    # Define the aggregation pipeline
    pipeline = [
        {"$match": {"phValue": "NULL"}}
    ]

    # Execute the aggregation pipeline query
    PH_NULL_value = collection1.aggregate(pipeline)

    # Add the query results to the context dictionary
    context = {"PH_NULL_value": PH_NULL_value}

    # Render the template with the context dictionary
    return render(request, "result7.html", context)

#Data that do not provide information about the resolution of protein structure

def result8(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB') 
    collection1 = Pdb.get_collection("structuralP1")

    # Define the aggregation pipeline
    pipeline = [
        {"$match": {"resolution": "NULL"}}
    ]

    # Execute the aggregation pipeline query
    RES_NULL_value = collection1.aggregate(pipeline)

    # Add the query results to the context dictionary
    context = {"RES_NULL_value": RES_NULL_value}

    # Render the template with the context dictionary
    return render(request, "result8.html", context)

#Sorting data by publication year in ascending order
def result9(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB') 
    collection1 = Pdb.get_collection("structuralP1")

    # Define the aggregation pipeline
    pipeline = [
        {"$sort": {"publicationYear": 1}}
    ]

    # Execute the aggregation pipeline query
    sort_year = collection1.aggregate(pipeline)

    # Add the query results to the context dictionary
    context = {"sort_year": sort_year}

    # Render the template with the context dictionary
    return render(request, "result9.html", context)

#Indexing data ascending based on publication year
def result10(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB') 
    collection1 = Pdb.get_collection("structuralP1")

    # Create an index on the collection
    collection1.create_index([("publicationYear", pymongo.ASCENDING)])

    # Define the aggregation pipeline
    pipeline = [{"$sort": {"publicationYear": 1}}]

    # Execute the aggregation pipeline query with a hint
    sort_year = collection1.aggregate(pipeline, hint="publicationYear_1")

    # Add the query results to the context dictionary
    context = {"sort_year": sort_year}

    # Render the template with the context dictionary
    return render(request, "result10.html", context)

# Obtaining proteins under neutral conditions

def result11(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB') 
    collection1 = Pdb.get_collection("structuralP1")

    # Execute the query
    docs_ph_neutral = collection1.find({"phValue": 7})

    # Render the template with the query results
    return render(request, "result11.html", {"docs_ph_neutral": docs_ph_neutral})


#Obtaining data with high structural resolution
def result12(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB') 
    collection1 = Pdb.get_collection("structuralP1")

    # Define the aggregation pipeline
    pipeline = [
        {"$match": {"$and": [{"resolution": {"$gte": 1}},{"resolution": {"$lt": 3}},{"macromoleculeType": "Protein"}]}}
    ]

    # Execute the aggregation pipeline query
    high_res_protein = collection1.aggregate(pipeline)

    # Render the template with the query results
    return render(request, "result12.html", {"high_res_protein": high_res_protein})

#Obtaining data with high structural resolution
def result13(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB') 
    collection1 = Pdb.get_collection("structuralP1")

    # Execute the MongoDB query
    high_res = collection1.find({"$and": [{"resolution": {'$gte':1}}, {"resolution": {'$lt':3}}]})

    # Render the template with the query results
    return render(request, "result13.html", {"high_res": high_res})


#Obtaining DNA with high structural resolution
def result14(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB') 
    collection1 = Pdb.get_collection("structuralP1")

    # Execute the MongoDB query
    high_res_DNA = collection1.find({"$and": [{"resolution": {"$gt": 1}},{"resolution":{'$lt':3}}, {"macromoleculeType": "DNA"}]})

    # Render the template with the query results
    return render(request, "result14.html", {"high_res_DNA": high_res_DNA})

#Obtaining proteins with poor structural resolution
def result15(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB') 
    collection1 = Pdb.get_collection("structuralP1")

    # Define the aggregation pipeline
    pipeline = [
        {
            "$match": {
                "resolution": {"$gte": 3}
            }
        }
    ]

    # Execute the aggregation pipeline query
    low_res = collection1.aggregate(pipeline)

    # Render the template with the query results
    return render(request, "result15.html", {"low_res": low_res})

#Isolating and analyzing large macromolecular complexes with high resolution
def result16(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB') 
    collection1 = Pdb.get_collection("structuralP1")

    # Define the aggregation pipeline
    pipeline = [
        {
            "$match": {
                "resolution": {"$gte": 3}
            }
        }
    ]

    # Execute the aggregation pipeline query
    low_res = collection1.aggregate(pipeline)

    # Render the template with the query results
    return render(request, "result16.html", {"low_res": low_res})

#Analyzing DNA data with X-ray diffraction
def result17(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB') 
    collection1 = Pdb.get_collection("structuralP1")

    # Define the aggregation pipeline
    pipeline = [
        {
            "$match": {
                "$and": [
                    {"resolution": {"$gte": 1}},
                    {"resolution": {"$lt": 3}},
                    {"residueCount": {"$gt": 100}}
                ]
            }
        }
    ]

    # Execute the aggregation pipeline query
    high_res_complx = collection1.aggregate(pipeline)

    # Render the template with the query results
    return render(request, "result17.html", {"high_res_complx": high_res_complx})


#Quantifying the amount of DNA/RNA hybrid

def result18(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB') 
    collection1 = Pdb.get_collection("structuralP1")

    # Define the aggregation pipeline
    pipeline = [
          {
               "$match": {
               "macromoleculeType": "DNA/RNA Hybrid"
               }
          },
          {
               "$count": "total_count"
          }
    ]
    # Execute the aggregation pipeline query
    result = list(collection1.aggregate(pipeline))
    count = result[0]['total_count']

    # Render the template with the query result
    return render(request, "result18.html", {"count": count})

#Advances in Understanding Oxygen Transport Since 1990
def result20(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB') 
    collection1 = Pdb.get_collection("structuralP1")

    # Execute the find query
    result = collection1.find({"$and": [{"publicationYear": {"$gt": 1990}}, {"classification": "OXYGEN TRANSPORT"}]})

    # Render the template with the query results
    return render(request, "result20.html", {"result": result})

#Organizing data in an ascending index based on ID
def result21(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB') 
    new1 = Pdb.get_collection("new1")
    collection1 = Pdb.get_collection("structuralP1")

    # Create an index on the _id field of the new1 collection
    new1.create_index([('_id', pymongo.ASCENDING)])

    # Retrieve all documents from the collection1 collection using the created index
    indexs = collection1.find().hint([('_id', 1)])

    # Render the template with the query results
    return render(request, "result21.html",{"indexs": indexs})

#Presenting DNA records
def result22(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB') 
    collection1 = Pdb.get_collection("structuralP1")

    # Execute the aggregate query
    DNA_matched = collection1.aggregate([{"$match": {"classification": "DNA"}}])

    # Render the template with the query results
    return render(request, "result22.html", {"DNA_matched": DNA_matched})

#Summation of molecular weights for each macromoleculeType
def result23(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB') 
    collection1 = Pdb.get_collection("structuralP1")

    # Execute the aggregation pipeline
    pipeline = [
        {"$group": {"_id": "$macromoleculeType", "total": {"$sum": "$structureMolecularWeight"}}},
        {"$project": {"_id": 0, "macromoleculeType": "$_id", "SumofstructureMolecularWeight": "$total"}}
    ]
    sum_of_MW = collection1.aggregate(pipeline)

    # Render the template with the query results
    return render(request, "result23.html", {"sum_of_MW": sum_of_MW})

#Determining the frequency of each macromolecule type in the records
def result24(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB') 
    collection1 = Pdb.get_collection("structuralP1")

    # Execute the aggregate query
    number_of_molecule = collection1.aggregate([
        {"$group": {"_id": "$macromoleculeType", "count": {"$sum": 1}}},
        {"$project": {"_id": 0, "macromoleculeType": "$_id", "Count": "$count"}}
    ])

    # Render the template with the query results
    return render(request, "result24.html", {"number_of_molecule": number_of_molecule})

#Count and classify data based on classification column
def result25(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB') 
    collection1 = Pdb.get_collection("structuralP1")

    # Execute the aggregate query
    classification_count = collection1.aggregate([
        {"$group": {"_id": "$classification", "count": {"$sum":1}}},
        {"$project": {"_id": 0, "classification": "$_id", "Sum": "$count"}}
    ])

    # Pass the query results to the template
    context = {"classification_count": classification_count}
    return render(request, "result25.html", context)


#Count and classify data based on experimentalTechnique column
def result26(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB')
    collection1 = Pdb.get_collection("structuralP1")

    # Execute the aggregate query
    technique_count = collection1.aggregate([
        {"$group": {"_id": "$experimentalTechnique", "count": {"$sum":1}}},
        {"$project": {"_id": 0, "experimentalTechnique": "$_id", "Sum": "$count"}}
    ])

    # Pass the query results to the template
    context = {"technique_count": technique_count}
    return render(request, "result26.html", context)


#Getting updated values from "NA" to "NULL"

def result111(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB') 
    collection1 = Pdb.get_collection("structuralP1")

    # Execute the aggregation pipeline to update documents
    pipeline = [
        {"$match": {"phValue": "NA"}},
        {"$addFields": {"phValue": "NULL"}}
    ]
    updated_docs = collection1.aggregate(pipeline)

    # Update documents using the update_many method
    filter_PH = {"phValue": "NA"}
    update = {"$set": {"phValue": "NULL"}}
    updated_PH = collection1.update_many(filter_PH, update)

    # Retrieve all documents from the collection
    all_doc = collection1.find()

    # Render the template with the updated documents
    return render(request, "result111.html", {"all_doc": all_doc})

#Obtaining the average weight of molecular structures
def result27(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB')
    collection1 = Pdb.get_collection("structuralP1")

    # Execute the aggregate query
    pipeline = [
        {"$group": {"_id": None, "average_MW_value": {"$avg": "$structureMolecularWeight"}}}
    ]
    AvgMW = collection1.aggregate(pipeline)
    average_value = AvgMW.next()["average_MW_value"]

    # Pass the query result to the template
    context = {"average_value": average_value}
    return render(request, "result27.html", context)

# Getting average resolution for data 
def result28(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB')
    collection1 = Pdb.get_collection("structuralP1")

    # Execute the aggregate query
    pipeline = [
        {"$group": {"_id": None, "average_res_value": {"$avg": "$resolution"}}}
    ]
    Avgres = collection1.aggregate(pipeline)
    average_value = Avgres.next()["average_res_value"]

    # Pass the query result to the template
    context = {"average_value": average_value}
    return render(request, "result28.html", context)

# Highest resolution value and its corresponding ID
def result29(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB')
    collection1 = Pdb.get_collection("structuralP1")

    # Execute the aggregate query
    pipeline = [
        {"$match": {"resolution": {"$ne": None}}},
        {"$sort": {"resolution": 1}},
        {"$limit": 1},
        {"$project": {"_id": 1, "resolution": 1}}
    ]
    highest_res_with_id = collection1.aggregate(pipeline)
    for doc in highest_res_with_id:
        highest_resolution_id = doc['_id']
        highest_resolution_value = doc['resolution']

    # Pass the query result to the template
    context = {"highest_resolution_id": highest_resolution_id, "highest_resolution_value": highest_resolution_value}
    return render(request, "result29.html", context)

# ID with the highest molecular weight and its corresponding value
def result30(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB')
    collection1 = Pdb.get_collection("structuralP1")

    # Execute the aggregate query
    pipeline = [
        {"$match": {"structureMolecularWeight": {"$ne": None}}},
        {"$sort": {"structureMolecularWeight": -1}},
        {"$limit": 1},
        {"$project": {"_id": 1, "structureMolecularWeight": 1}}
    ]
    max_MW_with_id = collection1.aggregate(pipeline)
    for doc in max_MW_with_id:
        max_MW_id = doc['_id']
        max_MW_value = doc['structureMolecularWeight']

    # Pass the query result to the template
    context = {"max_MW_id": max_MW_id, "max_MW_value": max_MW_value}
    return render(request, "result30.html", context)

# Finding all data in ProteinSeq collection
def result31(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB')
    collection2 = Pdb.get_collection("ProteinSeq")

    # Execute the find query
    all_docs = collection2.find()

    # Pass the query result to the template
    context = {"all_docs": all_docs}
    return render(request, "result31.html", context)

# Exploring the features of the 'CGCGAATTCGCG' sequence
def result32(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB')
    collection1 = Pdb.get_collection("structuralP1")
    collection2 = Pdb.get_collection("ProteinSeq")
    # Execute the reference relation query
    get_seq = collection2.find_one({"sequence": "CGCGAATTCGCG"})
    molecule_id = get_seq['structureId']
    pdb_str = collection1.find_one({'_id': molecule_id})

    # Pass the query result to the template
    context = {"pdb_str": pdb_str}
    return render(request, "result32.html", context)

# Retrieving information on the ID '101D
def result33(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    pdb = client.get_database('PDB')
    collection1 = pdb.get_collection('structralP1')
    collection2 = pdb.get_collection('ProteinSeq')

    # Execute the query to retrieve the molecule ID
    get_str_id = collection1.find_one({"_id": "101D"})
    molecule_id = get_str_id['_id']

    # Execute the query to retrieve the PDB data
    pdb_str = collection2.find({'structureId': molecule_id})

    # Create a list of PDB documents to pass to the template
    pdb_docs = [doc for doc in pdb_str]

    # Pass the data to the template
    context = {
        'pdb_docs': pdb_docs
    }
    return render(request, "result33.html", context)

# Creating proteinID_and_residueCountIndex index
def result34(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB')
    collection2 = Pdb.get_collection("ProteinSeq")

    # Create a compound index on the "ProteinSeq" collection
    collection2.create_index([("pID", DESCENDING), ("residueCount", ASCENDING)], name="proteinID_and_residueCountIndex")

    # Return a success message to the template
    context = {"message": "Compound index created successfully!"}
    return render(request, "result34.html", context)

# Removing the record with ID '101D'
def result35(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB')   
    collection1 = Pdb.get_collection("structuralP1")

    # Define the query filter
    dictOfData = {"_id": "101D"}

    # Delete one document from the "collection1" collection
    delete_result = collection1.delete_one(dictOfData)

    # Pass the number of deleted documents to the template
    context = {"deleted_count": delete_result.deleted_count}
    return render(request, "result35.html", context)

# Retrieving information on chain A of the ID '101D'
def result36(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    db = client.get_database('mydatabase')
    collection1 = db.get_collection('collection1')

    # Define the query filter
    query_filter = {"$and": [{"_id":"101D"}, {"ProteinSeq.chainId": "A"}]}

    # Find documents that match the query filter
    query_result = collection1.find(query_filter)

    # Pass the query result to the template
    context = {"query_result": query_result}
    return render(request, "result36.html", context)

# Arranging data in decreasing order by ID
def result37(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB')
    collection1 = Pdb.get_collection('structuralP1')

    # Create an index on the "PID" field of the "collection1" collection
    collection1.create_index([('PID', DESCENDING)])

    # Return a success message to the template
    context = {"message": "Index created successfully!"}
    return render(request, "result37.html", context)

# Retrieve Information on Chain A
def result38(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB')
    collection2 = Pdb.get_collection('ProteinSeq')

    # Find all documents with chainId "A" and return the query explanation
    query_result = collection2.find({"chainId": "A"}).explain()

    # Pass the query explanation to the template
    context = {"query_explanation": query_result}
    return render(request, "result38.html", context)

# Getting all data in structuralP1 collection
def result45(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    db = client.get_database('PDB')
    collection1 = db.get_collection('structuralP1')

    # Find all documents in the collection
    query_result = collection1.find()

    # Pass the query result to the template
    context = {"query_result": query_result}
    return render(request, "result45.html", context)

# Counting the deeting records  
def result43(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    db = client.get_database('PDB')
    collection1 = db.get_collection('structuralP1')

    # Define the list of data to delete
    list_of_data = {"_id": {"$in": ["107D","108D","109D","111D"]}}

    # Delete documents that match the query filter
    delete_result = collection1.delete_many(list_of_data)
    
    # Display the number of deleted documents in the template
    context = {"deleted_count": delete_result.deleted_count}
    return render(request, "result43.html", context)

# Accessing the updated data in the structuralP1 collection

# Removing multiple records identified by '107L', '107M', '108L', '108M'
def result44(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    db = client.get_database('mydatabase')
    collection1 = db.get_collection('collection1')

    # Define the list of data to delete
    list_of_data = {"_id": {"$in": ["107L","107M","108L","108M"]}}

    # Delete documents that match the query filter
    delete_result = collection1.delete_many(list_of_data)
    
    # Display the number of deleted documents in the template
    context = {"deleted_count": delete_result.deleted_count}
    return render(request, "result44.html", context)

# Retrieving the protein with ID 22 from the ProteinSeq collection in the structuralP1 collection
def result39(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    pdb = client.get_database('PDB')
    collection1 = pdb.get_collection('structuralP1')

    # Define the query filter with a specific ID
    id = 22
    query_filter = {'Details.pID': id}

    # Find documents that match the query filter
    query_result = collection1.find(query_filter)

    # Pass the query result to the template
    context = {"query_result": query_result}
    return render(request, "result39.html", context)

# Retrieving the protein with ID 32 from the ProteinSeq collection in the structuralP1 collection
def result40(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    db = client.get_database('PDB')
    collection1 = db.get_collection('structuralP1')

    # Define the query filter with a specific ID
    id = 32
    query_filter = {'Details.pID': id}

    # Find documents that match the query filter
    query_result = collection1.find(query_filter)

    # Pass the query result to the template
    context = {"query_result": query_result}
    return render(request, "result40.html", context)

# Listing out all the distinct classification categories in the data
def result41(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB')
    collection1 = Pdb.get_collection('structralP1')

    # Define the query filter with "$exists" operator
    query_filter = {"classification": {"$exists": True}}

    # Find documents that match the query filter
    query_result = collection1.find(query_filter)

    # Pass the query result to the template
    context = {"query_result": query_result}
    return render(request, "result41.html", context)

# Identifying and presenting all the IDs contained in the data
def result42(request):
    # Connect to the MongoDB database
    client = MongoClient(host='localhost', port=27017)
    Pdb = client.get_database('PDB') 
    collection1 = Pdb.get_collection("structuralP1")

    # Execute the query
    query = {"_id": {"$exists": True}}
    result = collection1.find(query)

    # Render the template with the query results
    return render(request, "result42.html", {"result": result})
