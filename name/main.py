from Pyro4 import naming, locateNS

if __name__ == "__main__":
    args = []
    flags = []
    if len(sys.argv)>1:
        for arg in sys.argv[1:]:
            if arg.startswith('--'): flags.append(arg[2:])
            elif arg=='-f': flags.append('force_restart')
            else: args.append(arg)
    try:
        ns = locateNS()
        
    except:
        sys.exit(naming.main())
