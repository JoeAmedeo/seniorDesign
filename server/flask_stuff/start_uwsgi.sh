if [ -e uwsgi.pi ]
   echo "It appears that uwsgi is already running, as the uwsgi.pid file exists. Use \"ps aux | grep \"uwsgi\"\" to investigate. May the force be with you."
else
    . venv/bin/activate
    uwsgi --ini /var/www/flask_app/flask_app_uwsgi.ini --pidfile uwsgi.pid &
    #this takes the "stopped" process, and puts it into background
    u_PID=$!
    kill -20 $u_PID
    kill -18 $u_PID
    echo "Press enter to finish re-enter your terminal"
fi
