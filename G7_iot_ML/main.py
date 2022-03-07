import base64
import argparse
from serverConnector import ServerConnector
serverConnector = ServerConnector()

def bootstrap(args):
    email = args["email"]
    password = args["password"]

    ServerConnector.token = serverConnector.auth(email, password)
    if args["mode"] == "pc":
        # run pc script
        print("PC mode")
        me = serverConnector.get_me()
        name = me.get("email").split("@")[0]
        with open(f"./data_img/1.{name}.jpeg", "wb") as fh:
            img_str = me.get("image").replace("data:image/jpeg;base64,", "")
            fh.write(base64.b64decode(img_str))
            from identification import Ident
            Ident()
    elif args["mode"] == "phone":
        # run phone script
        print("Phone mode")
        from objectDetection import ObjD
        ObjD(args["rtsp"])
    else:
        raise ("Unknown mode")

    
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode")
    parser.add_argument("--email")
    parser.add_argument("--password")
    parser.add_argument("--rtsp")
    args = vars(parser.parse_args())

    bootstrap(args)

"""
python main.py --mode phone --email student1@email.com --password 'toto11!!' --rtsp "rtsp://admin:admin@192.168.1.14:8554/live"
python3.7 main.py --mode pc --email student1@email.com --password 'toto11!!'
"""
