import logging

## logging setting
# Feature	            Using                   Using 
# Output Destination    filename='app.log'	    handlers=[...]
# 	                    Only the File.	        Multiple (File and Console).
# When you add exc_info=True, Python automatically captures the entire Stack Trace (the detailed error report showing exactly which line failed and why) and attaches it to the log.

logging.basicConfig(
    level=logging.INFO,
    # level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("app1.log"),
        logging.StreamHandler()
    ],
    force=True
)

logger=logging.getLogger("ArithmethicApp") # Logger Name

logger.info('Starting the application')

def add(a,b):
    result=a+b
    logger.debug(f"Adding {a} + {b}= {result}")
    return result

def subtract(a, b):
    result = a - b
    logger.debug(f"Subtracting {a} - {b} = {result}")
    return result

def multiply(a, b):
    result = a * b
    logger.debug(f"Multiplying {a} * {b} = {result}")
    return result

def divide(a, b):
    try:
        result = a / b
        logger.debug(f"Dividing {a} / {b} = {result}")
        return result
    except ZeroDivisionError:
        # logger.error("Division by zero error")
        logger.error("Division by zero error",exc_info=True)
        return None
    
add(10,15)
subtract(15,10)
multiply(10,20)
divide(20,0)