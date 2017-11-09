
#This is effectively a mutex.
if [ -e uwsgi_stopping.lock ]
then
    echo "uwsgi_stopping.lock exists. Can't execute the script. Someone else must be trying to stop the server."
elif [ -e uwsgi.pid ]
then
    echo "hello" | tee uwsgi_stopping.lock
    echo "The uwsgi.pid file exists. Yay!"
    . venv/bin/activate
    uwsgi --stop uwsgi.pid
    #check that the process has been killed
    u_pid="$(< uwsgi.pid)"
    if ps -p $u_pid > /dev/null
    then
	echo "The process wasn't killed using --stop. Will now forcekill"
	kill -9 $u_pid
    fi
    if ps -p $u_pid > /dev/null
    then
	echo "It couldn't forcekill the process. Weird"
    else
	echo "kill worked"
	rm uwsgi.pid
    fi
    rm uwsgi_stopping.lock
fi
