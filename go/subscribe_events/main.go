// Copyright © 2021 The Things Network Foundation, The Things Industries B.V.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// Example: subscribe_events
// Description: Subscribe to events for a particular device
// Usage: ./main [application-id] [device-id]

package main

import (
	"context"
	"crypto/tls"
	"flag"
	"fmt"
	"io"
	"os"

	"go.thethings.network/lorawan-stack/v3/pkg/log"
	"go.thethings.network/lorawan-stack/v3/pkg/rpcmetadata"
	"go.thethings.network/lorawan-stack/v3/pkg/rpcmiddleware/rpclog"
	"go.thethings.network/lorawan-stack/v3/pkg/ttnpb"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials"
)

var (
	grpcAddress = "eu1.cloud.thethings.network:8884" // gRPC server address for the Identity Server
	apiKey      = "NNSXS.XXXXXXXXXXXXXX.YYYYYYYYYYY" // Use a valid API key
	userAgent   = "myGoIntegration/v1.0.0"
)

func main() {
	flag.Parse()
	if flag.NArg() != 2 {
		fmt.Fprintf(os.Stderr, "Usage: %s [application-id] [device-id]", os.Args[0])
		os.Exit(1)
	}
	appID := flag.Arg(0)
	devID := flag.Arg(1)

	logger := log.NewLogger(
		log.WithLevel(log.DebugLevel),
		log.WithHandler(log.NewCLI(os.Stderr)),
	)
	rpclog.ReplaceGrpcLogger(logger)

	ctx := log.NewContext(context.Background(), logger)

	opts := []grpc.DialOption{
		grpc.WithTransportCredentials(credentials.NewTLS(&tls.Config{})),                  // require TLS
		grpc.WithPerRPCCredentials(rpcmetadata.MD{AuthType: "bearer", AuthValue: apiKey}), // set API key for authorization
		grpc.WithUserAgent(userAgent),                                                     // set user agent
	}
	cc, err := grpc.Dial(grpcAddress, opts...)
	if err != nil {
		logger.WithError(err).Fatal("Failed to connect to Identity Server")
	}

	stream, err := ttnpb.NewEventsClient(cc).Stream(ctx, &ttnpb.StreamEventsRequest{
		Identifiers: []*ttnpb.EntityIdentifiers{
			{
				Ids: &ttnpb.EntityIdentifiers_DeviceIDs{
					DeviceIDs: &ttnpb.EndDeviceIdentifiers{
						DeviceID: devID,
						ApplicationIdentifiers: ttnpb.ApplicationIdentifiers{
							ApplicationID: appID,
						},
					},
				},
			},
		},
	})
	if err != nil {
		logger.WithError(err).Fatal("Failed to subscribe to events")
	}
loop:
	for {
		event, err := stream.Recv()
		if err == io.EOF {
			break loop
		}
		if err != nil {
			logger.WithError(err).Fatal("Failed to retrieve message")
		}
		// Do something fancy with the event
		fmt.Println("New event:", event.Name)
	}
	fmt.Println("Done")
}
