import pika
import sys
import webbrowser
import csv
import time


host = "localhost"
smoker_temp_queue = '01-smoker'
food_a_temp_queue = '02-food-A'
food_b_temp_queue = '02-food-B'
data_file = 'smoker-temps.csv'
show_offer = True


def offer_rabbitmq_admin_site():
    if show_offer == True: 
        """Offer to open the RabbitMQ Admin website"""
        ans = input("Would you like to monitor RabbitMQ queues? y or n ")
        print()
        if ans.lower() == "y":
            webbrowser.open_new("http://localhost:15672/#/queues")
            print()

def delete_queue(host: str, queue_name: str):
    conn = pika.BlockingConnection(pika.ConnectionParameters(host))
    ch = conn.channel()
    ch.queue_delete(queue=queue_name)




def send_message(host: str, queue_name: str, message: str):
    """
    Creates and sends a message to the queue each execution.
    This process runs and finishes.

    Parameters:
        host (str): the host name or IP address of the RabbitMQ server
        queue_name (str): the name of the queue
        message (str): the message to be sent to the queue
    """

    try:
        # create a blocking connection to the RabbitMQ server
        conn = pika.BlockingConnection(pika.ConnectionParameters(host))
        # use the connection to create a communication channel
        ch = conn.channel()
        # use the channel to declare a durable queue
        # a durable queue will survive a RabbitMQ server restart
        # and help ensure messages are processed in order
        # messages will not be deleted until the consumer acknowledges
        ch.queue_declare(queue=queue_name, durable=True)
        # use the channel to publish a message to the queue
        # every message passes through an exchange
        ch.basic_publish(exchange="", routing_key=queue_name, body=message)
        # print a message to the console for the user
        print(f" [x] Sent {message}")
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error: Connection to RabbitMQ server failed: {e}")
        sys.exit(1)
    finally:
        # close the connection to the server
        conn.close()

def get_smoker_temps(file):
   
    #Define main body function
    file =  open(data_file,"r")
    # create a csv reader for our comma delimited data
    reader = csv.reader(file, delimiter=",")
    
    # skipping header row
    next(reader)
    

    for row in reader:
        fstring_time_column = f"{row[0]}"
    
    # since of of the columns are numbers, converting them to floats
    # convert to float       
        try:
            smoker_temp_channel1 = float(row[1])
            fstring_smoker_message = f"[{fstring_time_column}, {smoker_temp_channel1}]"
            smoker_temp_message = fstring_smoker_message.encode()
            send_message(host, smoker_temp_queue, smoker_temp_message)
        except ValueError:
            pass
        
       
        try:
            food_a_temp_channel2 = float(row[2])
            fstring_food_a_message = f"[{fstring_time_column}, {food_a_temp_channel2}]"
            food_a_temp_message = fstring_food_a_message.encode()
            send_message(host, food_a_temp_queue, food_a_temp_message)
        except ValueError:
            pass
          
        
        try:
            food_b_temp_channel3 = float(row[3])
            fstring_food_b_message = f"[{fstring_time_column}, {food_b_temp_channel3}]"
            food_b_temp_message = fstring_food_b_message.encode()
            send_message(host, food_b_temp_queue, food_b_temp_message)
        except ValueError:
           pass
       
        
    # sleep in seconds
        time.sleep(30)

# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":  
    # ask the user if they'd like to open the RabbitMQ Admin site
    offer_rabbitmq_admin_site(show_offer)
    
    
    delete_queue(host, smoker_temp_queue)
    delete_queue(host, food_a_temp_queue)
    delete_queue(host, food_b_temp_queue)
    
    get_data_from_csv(data_file)