
/*** block  from ../../../docs/manual/advanced-dataaccess.xml ***/
#include <string.h> /* for memset () */
#include <gst/gst.h>

static void
cb_handoff (GstElement *fakesrc,
	    GstBuffer  *buffer,
	    GstPad     *pad,
	    gpointer    user_data)
{
  static gboolean white = FALSE;
  GstMapInfo info;
  
  gst_buffer_map (buffer, &info, GST_MAP_WRITE);

  /* this makes the image black/white */
  memset (info.data, white ? 0xff : 0x0, info.size);
  white = !white;

  gst_buffer_unmap (buffer, &info);
}

gint
main (gint   argc,
      gchar *argv[])
{
  GstElement *pipeline, *fakesrc, *flt, *conv, *videosink;
  GMainLoop *loop;

  /* init GStreamer */
  gst_init (&argc, &argv);
  loop = g_main_loop_new (NULL, FALSE);

  /* setup pipeline */
  pipeline = gst_pipeline_new ("pipeline");
  fakesrc = gst_element_factory_make ("fakesrc", "source");
  flt = gst_element_factory_make ("capsfilter", "flt");
  conv = gst_element_factory_make ("videoconvert", "conv");
  videosink = gst_element_factory_make ("xvimagesink", "videosink");

  /* setup */
  g_object_set (G_OBJECT (flt), "caps",
  		gst_caps_new_simple ("video/x-raw",
				     "format", G_TYPE_STRING, "RGB16",
				     "width", G_TYPE_INT, 384,
				     "height", G_TYPE_INT, 288,
				     "framerate", GST_TYPE_FRACTION, 1, 1,
				     NULL), NULL);
  gst_bin_add_many (GST_BIN (pipeline), fakesrc, flt, conv, videosink, NULL);
  gst_element_link_many (fakesrc, flt, conv, videosink, NULL);

  /* setup fake source */
  g_object_set (G_OBJECT (fakesrc),
		"signal-handoffs", TRUE,
		"sizemax", 384 * 288 * 2,
		"sizetype", 2, NULL);
  g_signal_connect (fakesrc, "handoff", G_CALLBACK (cb_handoff), NULL);

  /* play */
  gst_element_set_state (pipeline, GST_STATE_PLAYING);
  g_main_loop_run (loop);

  /* clean up */
  gst_element_set_state (pipeline, GST_STATE_NULL);
  gst_object_unref (GST_OBJECT (pipeline));

  return 0;
}